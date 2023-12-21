import time
from kafka import KafkaConsumer
import datetime

"""
- handle auth mechanisms PLAINTEXT & SASL_PLAINTEXT
"""
consumer = KafkaConsumer('quickstart-events', bootstrap_servers='localhost:9092')
while True:
    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))
    time.sleep(1)
