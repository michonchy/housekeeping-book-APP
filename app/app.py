import os
import sys
import sqlalchemy as sql
def execute_cli():
    # コマンドライン引数(2つ目以降を取得
    # requirements.txt
    # 実行
    # pip install -r requirements.txt
    x=sys.argv[1:]
    print("値",x)
    print("型",type(x))
    db_dir = "../sql/house_keeping_book.sqlite"
    database_path = "sqlite:///" + os.path.abspath(db_dir)
    engine = sql.create_engine(database_path)
    print(engine)
    rows = engine.execute("select*from users;")
    print(rows)
    for row in rows:
        print(row)
if __name__=='__main__':
    execute_cli()