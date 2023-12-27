#!/usr/bin/env python

import os
import sys
import logging
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import \
    dispatch, StreamingCommand, Configuration, Option, validators

from solnlib import conf_manager
from kafka import KafkaProducer

ADDON_NAME = "publish_to_kafka"

logging.root.setLevel(logging.DEBUG)
# https://docs.python.org/3/library/logging.html#logrecord-attributes
formatter = logging.Formatter('%(levelname)s %(filename)s:L%(lineno)d:%(module)s:%(name)s:%(funcName)s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)

logger = logging.getLogger(__name__)


@Configuration()
class KafkaPublishCommand(StreamingCommand):

    def get_env_config_by_name(self, session_key: str, env_name: str):
        cfm = conf_manager.ConfManager(
            session_key,
            ADDON_NAME,
            realm=f"__REST_CREDENTIAL__#{ADDON_NAME}#configs/conf-publish_to_kafka_environment"
        )
        account_conf_file = cfm.get_conf("publish_to_kafka_environment")
        return account_conf_file.get(env_name)

    env_name = Option(
        doc='''**Description:** Stanza name of the Kafka environment''',
        require=False)
    topic_name = Option(
        doc='''**Description:** Kafka topic name''',
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

    def stream(self, records):
        self.logger.info(f"env name: {self.env_name}")
        session_key = vars(self.metadata.searchinfo)['session_key']
        env = self.get_env_config_by_name(session_key, self.env_name)
        bootstrap_servers = str(env['bootstrap_servers']).split(',')
        sasl_plain_password = env.get('sasl_plain_password')
        sasl_plain_username = env.get('sasl_plain_username')
        security_protocol = env.get('security_protocol')
        self.logger.info(f"bootstrap_servers={bootstrap_servers}")
        self.logger.info(f"security_protocol={security_protocol}")
        self.logger.info(f"sasl_plain_username={sasl_plain_username}")

        producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                 security_protocol=security_protocol,
                                 sasl_mechanism="PLAIN",
                                 sasl_plain_username=sasl_plain_username,
                                 sasl_plain_password=sasl_plain_password,
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                                 batch_size=self.batch_size,
                                 linger_ms=self.linger_ms)

        for record in records:
            producer.send(self.topic_name, record)
            yield record
        producer.flush(timeout=self.timeout)


dispatch(KafkaPublishCommand, sys.argv, sys.stdin, sys.stdout, __name__)
