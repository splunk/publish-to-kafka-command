#!/usr/bin/env python

import json
import logging
import logging.handlers
import os
import sys
import time
import hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import \
    dispatch, StreamingCommand, Configuration, Option, validators

from solnlib import conf_manager
import splunk

from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError, NoBrokersAvailable

ADDON_NAME = "publish_to_kafka"
LOG_PROGRESS_INTERVAL_SECONDS = 2

# WARNING: setting root log level to DEBUG severely slows overall performance
logging.root.setLevel(logging.INFO)


def setup_logging():
    # Log to index=_internal, source=LOGGING_FILE_NAME
    # https://dev.splunk.com/enterprise/docs/developapps/addsupport/logging/loggingsplunkextensions/
    logger = logging.getLogger()  # root logger
    SPLUNK_HOME = os.environ['SPLUNK_HOME']

    LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
    LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
    LOGGING_STANZA_NAME = 'python'
    LOGGING_FILE_NAME = "kafka_publish_command.log"
    BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
    LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
    splunk_log_handler = logging.handlers.RotatingFileHandler(
        os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a')
    splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    logger.addHandler(splunk_log_handler)
    splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
    return logger


setup_logging()


@Configuration()
class KafkaPublishCommand(StreamingCommand):
    env_name = Option(
        doc='Stanza name in publish_to_kafka_environment.conf',
        default=None,
        require=False)

    error_index_name = Option(
        doc='Index to write failed events to. If not specified, failed events will not be written to an index.',
        default=None,
        require=False)

    bootstrap_servers = Option(
        doc='Comma-separated list of bootstrap servers. Overrides environment config if specified.',
        require=False
    )
    sasl_plain_username = Option(
        doc='SASL PLAIN Auth Username. Overrides environment config if specified.',
        require=False
    )

    sasl_plain_password = Option(
        doc='SASL PLAIN Auth Password. Overrides environment config if specified.',
        require=False
    )

    security_protocol = Option(
        doc='Security Protocol. Overrides environment config if specified.',
        require=False,
        validate=validators.Set('PLAINTEXT', 'SASL_PLAINTEXT')
    )

    topic_name = Option(
        doc='Kafka topic name',
        require=True)

    linger_ms = Option(
        doc='Linger in milliseconds before sending messages to Kafka',
        require=False,
        default=0,
        validate=validators.Integer()
    )
    batch_size = Option(
        doc="""A small batch size will make batching less common and may reduce throughput 
        (a batch size of zero will disable batching entirely).""",
        require=False,
        default=16384,
        validate=validators.Integer()
    )
    timeout = Option(
        name='timeout',
        doc='Timeout for sending a message to Kafka (in seconds)',
        require=False,
        default=None,
        validate=validators.Integer()
    )

    def get_env_config_by_name(self, env_name: str):
        self.logger.info(f"env name: {self.env_name}")
        session_key = vars(self.metadata.searchinfo)['session_key']
        cfm = conf_manager.ConfManager(
            session_key,
            ADDON_NAME,
            realm=f"__REST_CREDENTIAL__#{ADDON_NAME}#configs/conf-publish_to_kafka_environment"
        )
        account_conf_file = cfm.get_conf("publish_to_kafka_environment")
        return account_conf_file.get(env_name)

    def get_config_value(self, env, key, optional=False):
        env_value = env.get(key)
        cmd_arg = getattr(self, key, None)
        if cmd_arg is not None and env_value is not None:
            self.write_warning(
                f"Using command argument {key}={cmd_arg} instead of environment config {key}={env_value}")

        if cmd_arg is not None:
            return cmd_arg
        elif env_value is not None:
            return env_value
        elif not optional:
            raise ValueError(f"Missing required argument: {key}")

    def get_producer_instance(self) -> KafkaProducer:
        env = {}
        if self.env_name is not None:
            env = self.get_env_config_by_name(self.env_name)

        producer_args = {
            "bootstrap_servers": self.get_config_value(env, "bootstrap_servers").split(','),
            "security_protocol": self.get_config_value(env, "security_protocol"),
            "sasl_plain_username": self.get_config_value(env, "sasl_plain_username", optional=True),
            "sasl_plain_password": self.get_config_value(env, "sasl_plain_password", optional=True),
            "sasl_mechanism": "PLAIN",
            "value_serializer": lambda x: json.dumps(x).encode('utf-8'),
            "batch_size": self.batch_size,
            "linger_ms": self.linger_ms,
        }
        for k, v in producer_args.items():
            if "password" in k:
                continue
            else:
                self.logger.info(f"KafkaProducer args {k}={v}")

        return KafkaProducer(**producer_args)

    def write_to_index(self, records):
        # Write failed records to an error index via oneshot upload to reduce network requests

        if self.error_index_name is None:
            return
        # Write all records to temp file
        import tempfile
        with tempfile.NamedTemporaryFile() as tmp:
            for record in records:
                tmp.write(json.dumps(record).encode('utf-8'))
                tmp.write(b'\n')
            tmp.flush()
            # Upload temp file to Splunk
            self.service.indexes[self.error_index_name].upload(tmp.name)

    def stream(self, records):
        # Note that records is a generator
        if self.error_index_name is not None and self.error_index_name not in self.service.indexes:
            raise ValueError(f"Index {self.error_index_name} does not exist")

        try:
            producer = self.get_producer_instance()
        except NoBrokersAvailable as e:
            raise RuntimeError("Bootstrap servers may be unreachable or credentials may be incorrect.") from e

        # converting to list may cause memory issues for very long events
        # Note that stream() receives up to 50,000 events
        records_list = list(records)
        record_indexes_received = set()

        def make_error_handler(failed_record):
            def handler(error):
                pass
                # self.logger.error(f"Error sending record to Kafka: {error} -> {failed_record}")

            return handler

        timestamp_send_start = time.time()
        last_log_time = timestamp_send_start

        def make_success_handler(record_index):
            def success_handler(record_metadata):
                nonlocal record_indexes_received
                nonlocal last_log_time

                record_indexes_received.add(record_index)
                time_elapsed = time.time() - timestamp_send_start
                time_since_last_log = time.time() - last_log_time
                records_per_second = len(record_indexes_received) / time_elapsed
                if time_since_last_log >= LOG_PROGRESS_INTERVAL_SECONDS:
                    self.logger.info(
                        f"Progress: metadata={record_metadata}, {len(record_indexes_received)} records sent in {time_elapsed:.3f} seconds.")
                    self.logger.info(f"Current performance: {records_per_second:.3f} records/second")
                    last_log_time = time.time()

            return success_handler

        for index, record in enumerate(records_list):
            # self.logger.info(f"Record: {index} -> {record}")
            producer.send(self.topic_name, record).add_errback(
                make_error_handler(record)
            ).add_callback(
                make_success_handler(index)
            )
            yield record

        try:
            producer.flush(timeout=self.timeout)
        except KafkaTimeoutError as e:
            self.logger.error(f"Timeout Error: {e}")
            num_failed = len(records_list) - len(record_indexes_received)
            self.logger.info(f"records_received={len(record_indexes_received)}. records_failed={num_failed}")
            self.write_error(f"{e}")

        if self.error_index_name is not None:
            failed_records = [record for index, record in enumerate(records_list) if index not in record_indexes_received]
            if failed_records:
                self.write_error(f"Failed to send {len(failed_records)} records to Kafka. Writing failed records to {self.error_index_name}")
                self.write_to_index(failed_records)


dispatch(KafkaPublishCommand, sys.argv, sys.stdin, sys.stdout, __name__)
