from sqlalchemy import Column, String, Float, Integer, DateTime
from database import Base

class Stock(Base):
    __tablename__ = "stocks"

    symbol = Column(String)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    datetime = Column(DateTime)