import os
import sys
from typing import List
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (Table, Column, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from database import DBSession
from models.user import User

Base = declarative_base()


def show_table(model_class_name: str):
    session = DBSession().issued()
    queried = session.query(globals()[model_class_name])
    all_model: List = queried.all()
    for model in all_model:
        print("---")
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
    elif subcommand == "read_sql":
        table_name = args[1]
        sql(f'SELECT * FROM {table_name}')
    elif subcommand == "sql":
        query = args[1]
        sql(query)


if __name__ == '__main__':
    execute_cli()
