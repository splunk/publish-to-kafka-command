#!/usr/bin/env python

import json
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import \
    dispatch, StreamingCommand, Configuration, Option, validators

from solnlib import conf_manager
from kafka import KafkaProducer

ADDON_NAME = "publish_to_kafka"

logging.root.setLevel(logging.DEBUG)


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
            "linger_ms": self.linger_ms
        }
        for k, v in producer_args.items():
            if "password" in k:
                continue
            else:
                self.logger.info(f"KafkaProducer args {k}={v}")

        return KafkaProducer(**producer_args)

    def write_to_index(self, records):
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
        if self.error_index_name is not None and self.error_index_name not in self.service.indexes:
            raise ValueError(f"Index {self.error_index_name} does not exist")

        producer = self.get_producer_instance()
        failed_records = []

        def make_error_handler(failed_record):
            def handler(error):
                self.logger.error(f"Error sending record to Kafka: {error}")
                self.logger.error(f"Record: {failed_record}")
                failed_records.append(failed_record)

            return handler

        for record in records:
            producer.send(self.topic_name, record).add_errback(make_error_handler(record))
            yield record

        producer.flush(timeout=self.timeout)

        if failed_records and self.error_index_name is not None:
            self.write_error(f"Failed to send {len(failed_records)} records to Kafka")
            # Write failed records to an error index via oneshot upload to reduce network requests
            self.write_to_index(failed_records)


dispatch(KafkaPublishCommand, sys.argv, sys.stdin, sys.stdout, __name__)
