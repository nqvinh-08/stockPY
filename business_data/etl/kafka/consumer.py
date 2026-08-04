import json
from kafka import KafkaConsumer
from business_data.etl.clean_data.clean_data import clean_data
from business_data.etl.store_data.load_data import load_data

consumer = KafkaConsumer(
    "stock_topic",
    bootstrap_servers="kafka:29092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="stock-group"
)

for msg in consumer:
    data = msg.value
    print("nhan du lieu tu kafka thanh cong")
    cleaned_data = clean_data(data)
    load_data(cleaned_data)
    print("luu du lieu vao clickhouse thanh cong")