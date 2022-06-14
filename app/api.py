import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer(),primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String())

app = Flask(__name__)

def create_engine():
    db_dir = "../sql/house_keeping_book.sqlite"
    database_path = "sqlite:///" + os.path.abspath(db_dir)
    engine = sqlalchemy.create_engine(database_path)
db = create_engine()
Session = sessionmaker(bind=db)
session = Session()

@app.route('/')
def hello():
    name = "Hello World"
    return name

@app.route('/good')
def good():
    name = "Good"
    return name

@app.route('/users')
def read_users():
    all_users = session.query(User).all()
    print(all_users)
    for user in all_users:
        print("---")
        print(user.id)
        print(user.name)
    return all_users[0]

## おまじない
if __name__ == "__main__":
    app.run(debug=True)