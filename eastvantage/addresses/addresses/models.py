from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class Address(Base):
    __tablename__  = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    note = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
