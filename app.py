import joblib
from pathlib import Path
import duckdb
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "olist.duckdb"
MODEL_PATH = BASE_DIR / "data" / "processed" / "delivery_risk_model.joblib"

@st.cache_data
def load_kpis():
    con = duckdb.connect(str(DB_PATH))
    df_kpis = con.execute("""
        SELECT
            COUNT(*) AS n_orders,
            AVG(delivery_days) AS avg_delivery_days,
            AVG(CASE WHEN delay_vs_estimate_days > 0 THEN 1 ELSE 0 END) AS late_rate
        FROM order_delivery_metrics;
    """).fetchdf()
    con.close()
    return df_kpis.iloc[0]

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

def main():
    st.write("✅ App started")
    st.title("Olist E-commerce Analytics & Delivery Risk Prediction")

    # KPIs
    st.header("Key Delivery KPIs")
    kpis = load_kpis()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total delivered orders", int(kpis["n_orders"]))
    col2.metric("Avg delivery days", f"{kpis['avg_delivery_days']:.1f}")
    col3.metric("Late delivery rate", f"{kpis['late_rate']*100:.1f}%")

    st.markdown("---")

    # Prediction form
    st.header("Predict Delivery Risk for a New Order")

    model = load_model()

    # For simplicity, ask user to type/choose feature values
    customer_state = st.selectbox("Customer state", options=[
        "SP", "RJ", "MG", "RS", "PR", "SC", "BA", "DF", "GO", "Other"
    ])
    seller_state = st.selectbox("Seller state", options=[
        "SP", "RJ", "MG", "RS", "PR", "SC", "BA", "DF", "GO", "Other"
    ])
    product_category = st.text_input("Product category name", value="bed_bath_table")
    price = st.number_input("Price (R$)", min_value=0.0, value=100.0, step=10.0)
    freight = st.number_input("Freight value (R$)", min_value=0.0, value=20.0, step=5.0)
    est_days = st.number_input("Estimated delivery days", min_value=1.0, value=7.0, step=1.0)
    purchase_dow = st.slider("Day of week of purchase (0=Mon, 6=Sun)", 0, 6, 2)
    purchase_month = st.slider("Month of purchase", 1, 12, 5)
    purchase_year = st.selectbox("Year of purchase", options=[2016, 2017, 2018])

    if st.button("Predict delivery risk"):
        # Build a single-row DataFrame
        data = pd.DataFrame([{
            "customer_state": customer_state,
            "seller_state": seller_state,
            "product_category_name": product_category,
            "price": price,
            "freight_value": freight,
            "estimated_delivery_days": est_days,
            "purchase_dow": purchase_dow,
            "purchase_month": purchase_month,
            "purchase_year": purchase_year
        }])

        proba_late = model.predict_proba(data)[0, 1]
        pred_label = "LATE" if proba_late >= 0.5 else "ON-TIME"

        st.subheader("Prediction")
        st.write(f"Predicted status: **{pred_label}**")
        st.write(f"Probability of being late: **{proba_late*100:.1f}%**")

if __name__ == "__main__":
    main()
