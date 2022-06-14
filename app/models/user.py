from sqlalchemy import (Table, Column, Integer, String)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer(),primary_key=True)
    name = Column(String())
    # staff_id = Column(Integer(), primary_key=True)
    # staff_name = Column(String(20), index=True)
    # staff_age = Column(Integer())
    # staff_section = Column(String(20))
    # staff_post = Column(String(20))