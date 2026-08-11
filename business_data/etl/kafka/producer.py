import json
from kafka import KafkaProducer
import os
from dotenv import load_dotenv
load_dotenv()


topic = os.getenv("KAFKA_TOPIC")
def send_to_kafka(data):
    producer= KafkaProducer(
        bootstrap_servers= os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    producer.send(topic, data)
    producer.flush()
    producer.close()
    print("gui du lieu vao kafka thanh cong")