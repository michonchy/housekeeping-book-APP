import json
import os
import sys
from typing import List
from requests import request
from requests import Request,Response
import requests
import sqlalchemy as sql
from database import DBSession
from models.entities import BaseEntity
from models.entities import User, Spending, Category, Income


def show_table(model_class_name: str):
    session = DBSession().issued()
    queried = session.query(globals()[model_class_name])
    all_model: List[BaseEntity] = queried.all()
    for model in all_model:
        print(model.__dict__)


def sql(query: str):
    session = DBSession().issued()
    rows = session.execute(query)
    print(rows)
    for row in rows:
        print(row)


def execute_cli():
    args = sys.argv[1:]
    if len(args) == 0:
        print("Please input a parameter.")
        return
    subcommand = args[0]
    if subcommand == "read":
        table_name = args[1]
        show_table(table_name)
    elif subcommand == "sql_read":
        table_name = args[1]
        sql(f'SELECT * FROM {table_name}')
    elif subcommand == "sql":
        query = args[1]
        sql(query)
    elif subcommand == "summary":
        response: Response = requests.get("http://127.0.0.1:5000/spendings")
        print(response.status_code)
        if response.status_code != 200:
            print("Invalid Response")
            return 
        d = json.loads(response.content)
        print(d["data"])
        spending_data = d["data"]
        summary = 0
        for spending in spending_data:
            summary -= spending["amount"]
        print(summary)

if __name__ == '__main__':
    execute_cli()
