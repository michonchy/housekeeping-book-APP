from typing import Type
from sqlalchemy import (ForeignKey, Table, Column, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm import relationship, Mapped


BaseEntity: Type[DeclarativeMeta] = declarative_base()


class User(BaseEntity):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    name = Column(String())


class Spending(BaseEntity):
    __tablename__ = "spendings"
    id = Column(Integer(), primary_key=True)
    amount = Column(Integer())
    date = Column(String())
    user_id: int = Column(ForeignKey("users.id"))
    user: Mapped[User] = relationship("User", backref="spendings")
