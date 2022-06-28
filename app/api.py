from crypt import methods
import datetime
import os
from pickle import PUT
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

@app.route('/users/<id>', methods=['GET'])
def read_user(id):
    session = DBSession().issued()
    queried: Query[User] = session.query(User)
    user: User = queried.filter_by(id=id).first()
    if not user:
        return jsonify({
            'code': 404,
        })
    ResponseData = TypedDict('UserResponse', {'id': int, 'name': str})
    result: ResponseData = {
        "id": user.id,
        "name": user.name
    }
    print(user)
    return jsonify({
        'code': 200,
        'data': result
    })


@app.route('/users', methods=['POST'])
def create_user():
    session = DBSession().issued()
    user = User(name = request.form["name"])
    session.add(user)
    session.commit()
    return jsonify({
        'code': 201,
    })


@app.route('/users/<id>',methods=['PUT'])
def put_user(id):
    session = DBSession().issued()
    queried: Query[User] = session.query(User)
    user: User = queried.filter_by(id=id).first()
    if not user:
        return jsonify({
            'code': 404,
        })
    if "name" in request.form:
        user.name = request.form["name"]
    session.commit()
    return jsonify({
        'code': 200,
    })

@app.route('/users/<id>',methods=['DELETE'])
def delete_user(id):
    session = DBSession().issued()
    found_user = session.query(User).filter_by(id=id).first()
    if not found_user:
        return jsonify({
            'code': 204,
        })
    session.delete(found_user)
    session.commit()
    return jsonify({
        'code': 200,
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


@app.route('/categories/<id>', methods=['GET'])
def read_category(id):
    session = DBSession().issued()
    queried: Query[Category] = session.query(Category)
    category: Category = queried.filter_by(id=id).first()
    if not category:
        return jsonify({
            'code': 404,
        })
    ResponseData = TypedDict('categoryResponse', {'id': int, 'name': str, 'color': str})
    result: ResponseData = {
        "id": category.id,
        "name": category.name,
        "color": category.color
    }
    print(category)
    return jsonify({
        'code': 200,
        'data': result
    })


@app.route('/categories', methods=['POST'])
def create_category():
    session = DBSession().issued()
    category = Category(name = request.form["name"])
    session.add(category)
    session.commit()
    return jsonify({
        'code': 201,
    })


@app.route('/categories/<id>',methods=['DELETE'])
def derete_category(id):
    session = DBSession().issued()
    found_category = session.query(Category).filter_by(id=id).first()
    if not found_category:
        return jsonify({
            'code': 204,
        })
    session.delete(found_category)
    session.commit()
    return jsonify({
        'code': 200,
    })

@app.route('/spendings', methods=['GET'])
def read_spendings():
    year = request.args.get("year")
    month = request.args.get("month")
    print(year,month)
    session = DBSession().issued()
    queried: Query[Spending] = session.query(Spending)
    spendings: List[Spending] = []
    if year and month :
        y = int(year)
        m = int(month)
        from_date = datetime.date(y, m, 1)
        to_date = datetime.date(
            y + 1 if m == 12 else y,
            1 if m == 12 else m + 1,
            1
        )
        spendings = queried.filter(
            sqlalchemy.and_(Spending.date >= from_date,
                Spending.date < to_date))
    else:
        spendings = queried.all()
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


@app.route('/spendings/<id>', methods=['GET'])
def read_spending(id):
    session = DBSession().issued()
    queried: Query[Spending] = session.query(Spending)
    spending: Spending = queried.filter_by(id=id).first()
    if not spending:
        return jsonify({
            'code': 404,
        })
    UserData = TypedDict('UserData', {'id': int, 'name': str})
    CategoryData = TypedDict('CategoryData', {'id': int, 'name': str, 'color':str})
    ResponseData = TypedDict('SpendingResponse', {'id': int, 'amount': int, 'date': str, 'user': UserData, 'category': CategoryData})
    result: ResponseData = {
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
    }
    print(spending)
    return jsonify({
        'code': 200,
        'data': result
    })

@app.route('/spndings/<id>',methods=['DELETE'])
def derete_spending(id):
    session = DBSession().issued()
    found_spending = session.query(Spending).filter_by(id=id).first()
    if not found_spending:
        return jsonify({
            'code': 204,
        })
    session.delete(found_spending)
    session.commit()
    return jsonify({
        'code': 200,
    })


@app.route('/incomes', methods=['GET'])
def read_incomes():
    year = request.args.get("year")
    month = request.args.get("month")
    session = DBSession().issued()
    queried: Query[Income] = session.query(Income)
    incomes: List[Income] = []
    if year and month :
        y = int(year)
        m = int(month)
        from_date = datetime.date(y, m, 1)
        to_date = datetime.date(
            y + 1 if m == 12 else y,
            1 if m == 12 else m + 1,
            1
        )
        incomes = queried.filter(
            sqlalchemy.and_(Income.date >= from_date,
                Income.date < to_date))
    else:
        incomes = queried.all()
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


@app.route('/incomes/<id>', methods=['GET'])
def read_income(id):
    session = DBSession().issued()
    queried: Query[Income] = session.query(Income)
    income: Income = queried.filter_by(id=id).first()
    if not income:
        return jsonify({
            'code': 404,
        })
    UserData = TypedDict('UserData', {'id': int, 'name': str})
    CategoryData = TypedDict('CategoryData', {'id': int, 'name': str, 'color':str})
    ResponseData = TypedDict('IncomeResponse', {'id': int, 'amount': int, 'date': str, 'user': UserData, 'category': CategoryData})
    result: ResponseData = {
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
    }
    print(income)
    return jsonify({
        'code': 200,
        'data': result
    })


@app.route('/incomes/<id>',methods=['DELETE'])
def derete_sincome(id):
    session = DBSession().issued()
    found_income = session.query(Income).filter_by(id=id).first()
    if not found_income:
        return jsonify({
            'code': 204,
        })
    session.delete(found_income)
    session.commit()
    return jsonify({
        'code': 200,
    })



if __name__ == "__main__":
    app.run(debug=True)