CREATE OR REPLACE TABLE order_delivery_metrics AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    -- Cast to timestamps
    CAST(o.order_purchase_timestamp AS TIMESTAMP) AS purchase_ts,
    CAST(o.order_delivered_customer_date AS TIMESTAMP) AS delivered_ts,
    CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS estimated_ts,
    -- Delivery times in days
    datediff('day', purchase_ts, delivered_ts) AS delivery_days,
    datediff('day', purchase_ts, estimated_ts) AS estimated_delivery_days,
    datediff('day', estimated_ts, delivered_ts) AS delay_vs_estimate_days
FROM orders o
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL;
