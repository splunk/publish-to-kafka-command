import time
from kafka import KafkaProducer
import datetime

producer = KafkaProducer(bootstrap_servers='localhost:29092')
for _ in range(5):
    my_str = f"hello world {datetime.datetime.now()}"
    producer.send('quickstart-events', my_str.encode('utf-8'))
    time.sleep(1)
