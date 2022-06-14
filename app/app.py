import os
import sys
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (Table, Column, Integer, String)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer(),primary_key=True)
    name = Column(String())


def show_table(engine, table_name: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    all_users = session.query(User).all()
    print(all_users)
    for user in all_users:
        print("---")
        print(user.id)
        print(user.name)

    # rows = engine.execute(f"select*from {table_name};")
    # rows = engine.execute(f"select*from users;")
    # print(rows)
    # for row in rows:
    #     print("---")
    #     print(row[0])
    #     print(row[1])

def execute_cli():
    # コマンドライン引数(2つ目以降を取得
    # requirements.txt
    # 実行
    # pip install -r requirements.txt
    args=sys.argv[1:]
    if len(args) == 0:
        print("Please input a parameter.")
        return 
    subcommand = args[0]
    db_dir = "../sql/house_keeping_book.sqlite"
    database_path = "sqlite:///" + os.path.abspath(db_dir)
    engine = sql.create_engine(database_path)
    if subcommand == "read":
        table_name = args[1]
        show_table(engine, table_name)

if __name__=='__main__':
    execute_cli()