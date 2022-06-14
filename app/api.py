import os
from re import A
import sqlite3
from typing import List, TypedDict
from requests import Session
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from flask import Flask, g, jsonify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as BaseSession
from sqlalchemy.orm.query import Query
from models.user import User

Base = declarative_base()

app = Flask(__name__)

_db: sqlalchemy.engine.Engine


def _created_db():
    if 'db' not in g:
        db_dir = "../sql/house_keeping_book.sqlite"
        database_path = "sqlite:///" + os.path.abspath(db_dir)
        _db = sqlalchemy.create_engine(database_path)
    return _db


def db_session() -> BaseSession:
    Session = sessionmaker(bind=_created_db())
    session: BaseSession = Session()
    return session


@app.route('/')
def hello():
    name = "Hello World"
    return name


@app.route('/good')
def good():
    name = "Good"
    return name


@app.route('/users', methods=['GET'])
def read_users():
    session = db_session()
    queried: Query[User] = session.query(User)
    users: List[User] = queried.all()
    ResponseData = TypedDict('UserResponse', {'id': int, 'name': str})
    result: List[ResponseData] = []
    print(users)
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name
        })
    return jsonify({
        'code': 200,
        'data': result
    })


if __name__ == "__main__":
    app.run(debug=True)
