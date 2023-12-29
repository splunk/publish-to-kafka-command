import time
from kafka import KafkaProducer
import datetime

"""
- handle auth mechanisms PLAINTEXT & SASL_PLAINTEXT
"""
producer = KafkaProducer(bootstrap_servers=['localhost:9094'],
                         security_protocol="SASL_PLAINTEXT",
                         sasl_mechanism="PLAIN",
                         sasl_plain_username="user1",
                         sasl_plain_password="password1")
TOPIC_NAME = "test"
for _ in range(5):
    my_str = f"hello world {datetime.datetime.now()}"
    producer.send(TOPIC_NAME, my_str.encode('utf-8'))
    time.sleep(0.5)
