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
def get_spending_data(query: str):
    response: Response = requests.get("http://127.0.0.1:5000/spendings" + query)
    if response.status_code != 200:
        print("Invalid Response")
        raise Exception("Invalid Response")
    d = json.loads(response.content)
    spending_data = d["data"]
    return spending_data

def get_income_data(query: str):
    response: Response = requests.get("http://127.0.0.1:5000/incomes" + query)
    if response.status_code != 200:
        print("Invalid Response")
        raise Exception("Invalid Response") 
    d = json.loads(response.content)
    income_data = d["data"]
    return income_data

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
        month = None
        query = ""
        if len(args) > 1:
            input_date = args[1].split("/")
            year = input_date[0]
            month = input_date[1]
            query = "?year=" + year + "&month=" + month
        spending_data = get_spending_data(query)
        income_data = get_income_data(query)
        summary = 0
        for spending in spending_data:
             summary -= spending["amount"]
        for income in income_data:
            summary += income["amount"]
        print(summary)

if __name__ == '__main__':
    execute_cli()
