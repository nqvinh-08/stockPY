import json
from kafka import KafkaProducer
import os
from dotenv import load_dotenv
load_dotenv()

producer= KafkaProducer(
    bootstrap_servers= os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
topic = os.getenv("KAFKA_TOPIC")
def send_to_kafka(data):
    producer.send(topic, data)
    producer.flush()
    print("gui du lieu vao kafka thanh cong")