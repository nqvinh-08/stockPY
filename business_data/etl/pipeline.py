
from dotenv import load_dotenv
from business_data.etl.crawler.fetch_stock import fetch_stock
from business_data.etl.transform.clean_data import clean_data
from business_data.etl.load.load_data import load_data

load_dotenv()

raw_data = fetch_stock()
cleaned_data = clean_data(raw_data)
load_data(cleaned_data)