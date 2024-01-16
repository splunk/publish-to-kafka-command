#!/usr/bin/env python

import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import \
    dispatch, StreamingCommand, Configuration

import requests

logging.root.setLevel(logging.DEBUG)


@Configuration()
class HelloWorldCommand(StreamingCommand):
    def my_ip(self):
        resp = requests.get('https://api.ipify.org?format=json')
        ip = resp.json()['ip']
        msg = f"My ip address is {ip}"
        self.logger.error(msg)
        self.write_error(msg)

    def stream(self, records):
        self.my_ip()
        for record in records:
            yield record


dispatch(HelloWorldCommand, sys.argv, sys.stdin, sys.stdout, __name__)
