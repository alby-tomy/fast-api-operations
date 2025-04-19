from sqlalchemy import Column, Integer, String
from database import Base

class UserProfile(Base):
    __tablename__ = "user_profile"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    profession = Column(String)

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True, nullable=False)
    country_code = Column(String, nullable=False)
    product_quantity_number = Column(Integer, nullable=False)
