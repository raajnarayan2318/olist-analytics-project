import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "olist.duckdb"

con = duckdb.connect(str(DB_PATH))

# 1) Basic: how many customers?
df_customers = con.execute("SELECT COUNT(*) AS n_customers FROM customers").fetchdf()
print(df_customers)

# 2) Orders by status
df_status = con.execute("""
    SELECT order_status, COUNT(*) AS n_orders
    FROM orders
    GROUP BY order_status
    ORDER BY n_orders DESC;
""").fetchdf()
print(df_status)

# 3) Average order value (AOV) by payment type
df_aov = con.execute("""
    SELECT
        p.payment_type,
        AVG(p.payment_value) AS avg_payment,
        COUNT(DISTINCT p.order_id) AS n_orders
    FROM order_payments p
    GROUP BY p.payment_type
    ORDER BY avg_payment DESC;
""").fetchdf()
print(df_aov)

con.close()
