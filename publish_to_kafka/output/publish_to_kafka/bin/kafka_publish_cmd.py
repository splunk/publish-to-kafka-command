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
# https://docs.python.org/3/library/logging.html#logrecord-attributes
# formatter = logging.Formatter('%(levelname)s %(filename)s:L%(lineno)d:%(module)s:%(name)s:%(funcName)s %(message)s')
# handler = logging.StreamHandler()
# handler.setFormatter(formatter)
# logging.root.addHandler(handler)
#
# logger = logging.getLogger(__name__)


@Configuration()
class KafkaPublishCommand(StreamingCommand):
    env_name = Option(
        doc='Stanza name in publish_to_kafka_environment.conf',
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

    def stream(self, records):
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
        producer = KafkaProducer(**producer_args)

        for record in records:
            producer.send(self.topic_name, record)
            yield record
        producer.flush(timeout=self.timeout)


dispatch(KafkaPublishCommand, sys.argv, sys.stdin, sys.stdout, __name__)
