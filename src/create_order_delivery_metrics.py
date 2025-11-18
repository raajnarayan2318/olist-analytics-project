import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "olist.duckdb"
SQL_PATH = BASE_DIR / "sql" / "order_delivery_metrics.sql"

def main():
    con = duckdb.connect(str(DB_PATH))
    with open(SQL_PATH, "r") as f:
        sql = f.read()
    con.execute(sql)
    result = con.execute("SELECT COUNT(*) AS n FROM order_delivery_metrics").fetchdf()
    print(result)
    con.close()

if __name__ == "__main__":
    main()
