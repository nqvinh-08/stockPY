import logging
from dotenv import load_dotenv
from business_data.etl.crawler.fetch_stock import fetch_stock
from business_data.etl.kafka.producer import send_to_kafka

load_dotenv()

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run():
    logging.info("bat dau lay dlieu")
    raw_data = fetch_stock()
    logging.info("lay xong")
    send_to_kafka(raw_data)
    logging.info("gui vao kafka thanh cong")
if __name__ =="__main__":
    run()