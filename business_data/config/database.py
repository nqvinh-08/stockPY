import os
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client():
    global _client

    if _client is None:
        _client = clickhouse_connect.get_client(
            host=os.getenv("HOSTCLICKHOUSE"),
            port=int(os.getenv("PORTCLICKHOUSE")),
            username=os.getenv("USERCLICKHOUSE"),
            password=os.getenv("PASSCLICKHOUSE"),
            database=os.getenv("DATABASECLICKHOUSE"),
        )

    return _client