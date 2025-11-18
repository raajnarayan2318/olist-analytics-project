# Olist E-commerce Analytics & Delivery Risk Prediction

## Overview
This project analyzes the Brazilian E-Commerce Public Dataset by Olist and builds
a machine learning model to predict late deliveries (delivery risk).
It combines SQL (DuckDB), Python (pandas, scikit-learn), and a Streamlit app.

## Business questions
- How long do deliveries take on average?
- How often are deliveries late vs estimated delivery date?
- How does lateness affect customer review scores?
- Can we predict the probability that a new order will be delivered late?

## Tech stack
- Python 3.11, pandas, scikit-learn, matplotlib, plotly
- DuckDB for SQL-based data modeling
- Streamlit for an interactive dashboard

## Project structure
- `data/raw/` – raw CSV files from the Olist dataset (not committed to repo)
- `data/processed/` – processed datasets & saved model
- `src/init_db.py` – load CSV into DuckDB
- `src/create_order_delivery_metrics.py` – build delivery metrics table
- `src/build_ml_dataset.py` – create ML-ready dataset
- `src/train_model.py` – train and evaluate model
- `app.py` – Streamlit app for KPIs and delivery risk prediction
- `notebooks/` – exploratory notebooks (EDA, experiments)

## How to run

### 1. Create environment and install dependencies
```bash
conda create -n olist-env python=3.11 -y
conda activate olist-env
pip install -r requirements.txt
