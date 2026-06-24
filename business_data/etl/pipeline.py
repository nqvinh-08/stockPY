import logging
from dotenv import load_dotenv
from business_data.etl.crawler.fetch_stock import fetch_stock
from business_data.etl.transform.clean_data import clean_data
from business_data.etl.load.load_data import load_data

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run():
    logging.info("bat dau lay dlieu")
    raw_data = fetch_stock()
    logging.info("lam sach")
    cleaned_data = clean_data(raw_data)
    logging.info("luu")
    load_data(cleaned_data)
    logging.info("done")
if __name__ =="__main__":
    run()