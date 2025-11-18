import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "olist.duckdb"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "ml_delivery_dataset.parquet"

def main():
    con = duckdb.connect(str(DB_PATH))

    # Join orders + items + customers + sellers + products + our delivery metrics
    query = """
    CREATE OR REPLACE TABLE ml_delivery_dataset AS
    SELECT
        odm.order_id,
        c.customer_unique_id,
        c.customer_state,
        s.seller_state,
        p.product_category_name,
        i.price,
        i.freight_value,
        odm.delivery_days,
        odm.estimated_delivery_days,
        (odm.delay_vs_estimate_days > 0) AS is_late,
        -- Date features
        DATE_TRUNC('day', odm.purchase_ts) AS purchase_date,
        EXTRACT(dayofweek FROM odm.purchase_ts) AS purchase_dow,
        EXTRACT(month FROM odm.purchase_ts) AS purchase_month,
        EXTRACT(year FROM odm.purchase_ts) AS purchase_year
    FROM order_delivery_metrics odm
    JOIN order_items i ON odm.order_id = i.order_id
    JOIN customers c ON odm.customer_id = c.customer_id
    JOIN sellers s ON i.seller_id = s.seller_id
    JOIN products p ON i.product_id = p.product_id
    WHERE odm.delivery_days IS NOT NULL
      AND odm.estimated_delivery_days IS NOT NULL;
    """

    con.execute(query)

    # Export to parquet for convenient use in pandas
    con.execute(f"""
        COPY (SELECT * FROM ml_delivery_dataset)
        TO '{OUTPUT_PATH.as_posix()}'
        (FORMAT PARQUET);
    """)

    con.close()
    print(f"ML dataset saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
