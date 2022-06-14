from sqlalchemy.engine import create_engine, Engine as DBEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as BaseSession
import os


class DBSession(object):
    _db: DBEngine

    def __init__(self) -> None:
        db_dir = "../sql/house_keeping_book.sqlite"
        database_path = "sqlite:///" + os.path.abspath(db_dir)
        self._db = create_engine(database_path)

    def issued(self):
        Session = sessionmaker(bind=self._db)
        session: BaseSession = Session()
        return session
