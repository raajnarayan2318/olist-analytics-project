import duckdb
from pathlib import Path

# 1. Paths
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DB_PATH = BASE_DIR / "data" / "olist.duckdb"

def main():
    # 2. Connect to DuckDB (creates file if not exists)
    con = duckdb.connect(str(DB_PATH))

    # 3. Create tables by reading CSVs
    # DuckDB can create a table directly from a CSV read
    def create_table_from_csv(table_name: str, file_name: str):
        csv_path = DATA_RAW_DIR / file_name
        print(f"Loading {file_name} into table {table_name}...")
        con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT * FROM read_csv_auto('{csv_path.as_posix()}', HEADER=TRUE);
        """)

    create_table_from_csv("customers", "olist_customers_dataset.csv")
    create_table_from_csv("orders", "olist_orders_dataset.csv")
    create_table_from_csv("order_items", "olist_order_items_dataset.csv")
    create_table_from_csv("order_payments", "olist_order_payments_dataset.csv")
    create_table_from_csv("order_reviews", "olist_order_reviews_dataset.csv")
    create_table_from_csv("products", "olist_products_dataset.csv")
    create_table_from_csv("sellers", "olist_sellers_dataset.csv")
    create_table_from_csv("geolocation", "olist_geolocation_dataset.csv")

    # 4. Quick sanity check
    result = con.execute("SELECT COUNT(*) AS n_orders FROM orders").fetchdf()
    print(result)

    con.close()
    print(f"Database created at {DB_PATH}")

if __name__ == "__main__":
    main()
