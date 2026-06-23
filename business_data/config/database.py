import os
import logging
import clickhouse_connect
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

try:
    client = clickhouse_connect.get_client(
        host=os.getenv("HOSTCLICKHOUSE"),
        port=int(os.getenv("PORTCLICKHOUSE")),
        username=os.getenv("USERCLICKHOUSE"),
        password=os.getenv("PASSCLICKHOUSE"),
        database=os.getenv("DATABASECLICKHOUSE"),
    )
    logger.info(" Kết nối ClickHouse database thành công")
except Exception as e:
    logger.error(f" Lỗi kết nối database: {str(e)}", exc_info=True)
    raise