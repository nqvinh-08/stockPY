import datetime
from pydantic import BaseModel

class Stock(BaseModel):
    symbol: str
    open: float
    close: float
    high: float
    low: float
    volume: int
    datetime: datetime
