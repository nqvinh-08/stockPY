from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = "user"

    username = Column(String)
    password = Column(String)