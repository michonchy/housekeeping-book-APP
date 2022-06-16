import os
from re import A
import sqlite3
from typing import List, TypedDict
from unicodedata import category
from requests import Session
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from flask import Flask, g, jsonify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as BaseSession
from sqlalchemy.orm.query import Query
from database import DBSession
from models.entities import Category, Income, Spending, User
from flask import request

Base = declarative_base()

app = Flask(__name__)


@app.route('/')
def hello():
    name = "Hello World"
    return name


@app.route('/users', methods=['GET'])
def read_users():
    session = DBSession().issued()
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


@app.route('/users', methods=['POST'])
def create_users():
    session = DBSession().issued()
    user = User(name = request.form["name"])
    session.add(user)
    session.commit()
    return jsonify({
        'code': 201,
    })


@app.route('/categories', methods=['GET'])
def read_categories():
    session = DBSession().issued()
    queried: Query[Category] = session.query(Category)
    categories: List[Category] = queried.all()
    ResponseData = TypedDict('CategoryResponse', {'id': int, 'name': str, 'color': str})
    result: List[ResponseData] = []
    print(categories)
    for category in categories:
        result.append({
            "id": category.id,
            "name": category.name,
            "color": category.color
        })
    return jsonify({
        'code': 200,
        'data': result
    })


@app.route('/categories', methods=['POST'])
def create_categories():
    session = DBSession().issued()
    category = Category(name = request.form["name"])
    session.add(category)
    session.commit()
    return jsonify({
        'code': 201,
    })

@app.route('/spendings', methods=['GET'])
def read_spendings():
    session = DBSession().issued()
    queried: Query[Spending] = session.query(Spending)
    spendings: List[Spending] = queried.all()
    UserData = TypedDict('UserData', {'id': int, 'name': str})
    CategoryData = TypedDict('CategoryData', {'id': int, 'name': str, 'color':str})
    ResponseData = TypedDict('SpendingResponse', {'id': int, 'amount': int, 'date': str, 'user': UserData, 'category': CategoryData})
    result: List[ResponseData] = []
    print(spendings)
    for spending in spendings:
        result.append({
            "id": spending.id,
            "amount": spending.amount,
            "date": spending.date,
            "user": {
                "id": spending.user.id,
                "name": spending.user.name
            },
            "category": {
                "id": spending.category.id,
                "name": spending.category.name,
                "color": spending.category.color 
            }
        })
    return jsonify({
        'code': 200,
        'data': result
    })


@app.route('/incomes', methods=['GET'])
def read_incomes():
    session = DBSession().issued()
    queried: Query[Income] = session.query(Income)
    incomes: List[Income] = queried.all()
    UserData = TypedDict('UserData', {'id': int, 'name': str})
    CategoryData = TypedDict('CategoryData', {'id': int, 'name': str, 'color':str})
    ResponseData = TypedDict('SpendingResponse', {'id': int, 'amount': int, 'date': str, 'user': UserData, 'category': CategoryData})
    result: List[ResponseData] = []
    print(incomes)
    for income in incomes:
        result.append({
            "id": income.id,
            "amount": income.amount,
            "date": income.date,
            "user": {
                "id": income.user.id,
                "name": income.user.name
            },
            "category": {
                "id": income.category.id,
                "name": income.category.name,
                "color": income.category.color 
            }
        })
    return jsonify({
        'code': 200,
        'data': result
    })

if __name__ == "__main__":
    app.run(debug=True)
