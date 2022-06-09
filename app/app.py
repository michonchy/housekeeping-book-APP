import os
import sys
import sqlalchemy as sql

def show_table(engine, table_name: str):
    rows = engine.execute(f"select*from {table_name};")
    print(rows)
    for row in rows:
        print(row)

def execute_cli():
    # コマンドライン引数(2つ目以降を取得
    # requirements.txt
    # 実行
    # pip install -r requirements.txt
    args=sys.argv[1:]
    subcommand = args[0]
    db_dir = "../sql/house_keeping_book.sqlite"
    database_path = "sqlite:///" + os.path.abspath(db_dir)
    engine = sql.create_engine(database_path)
    show_table(engine, subcommand)

if __name__=='__main__':
    execute_cli()