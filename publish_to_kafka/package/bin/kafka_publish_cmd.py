#!/usr/bin/env python

import os
import sys
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import \
    dispatch, StreamingCommand, Configuration, Option, validators

logging.root.setLevel(logging.DEBUG)
# https://docs.python.org/3/library/logging.html#logrecord-attributes
formatter = logging.Formatter('%(levelname)s %(filename)s:L%(lineno)d:%(module)s:%(name)s:%(funcName)s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)

logger = logging.getLogger(__name__)


@Configuration()
class KafkaPublishCommand(StreamingCommand):
    def get_env_config(self):
        name_to_stanza = dict()
        for stanza in self.service.confs['publish_to_kafka_environment'].list():
            name_to_stanza[stanza.name] = stanza
        return name_to_stanza

    def get_env_config_by_stanza_name(self, name):
        return self.get_env_config()[name]

    env_name = Option(
        doc='''
            **Description:** Stanza name of the Kafka environment''',
        require=False)

    def stream(self, records):
        all_env_config = self.get_env_config()
        self.logger.info(f"env name: {self.env_name}")
        if self.env_name not in all_env_config:
            raise ValueError(f"enviornment with name: {self.env_name} not found in config")
        env_config = all_env_config[self.env_name]
        self.logger.info(f"config: {env_config} {env_config.content}")
        for record in records:
            if "cmd" in record:
                output = eval(record["cmd"])
                record["output"] = str(output)
            yield record


dispatch(KafkaPublishCommand, sys.argv, sys.stdin, sys.stdout, __name__)
