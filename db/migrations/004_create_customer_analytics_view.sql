CREATE VIEW IF NOT EXISTS v_customer_analytics AS
WITH customer_base AS (
    SELECT
        c.customer_id,
        c.name,
        c.country,
        COUNT(DISTINCT o.order_id)                  AS completed_orders_count,
        COALESCE(SUM(oi.quantity * oi.price), 0.0)  AS total_spend,
        MAX(o.order_date) AS last_order_date

    FROM customers c

    LEFT JOIN orders o
        ON c.customer_id = o.customer_id
        AND o.status = 'COMPLETED'

    LEFT JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY c.customer_id, c.name, c.country
)

SELECT
    customer_id,
    name,
    country,
    completed_orders_count,
    total_spend,
    last_order_date,

    /* Ranks customers by spend without skipping rank numbers when two customers tie (e.g., Charlie and Evan both tied at $0.00 receive rank 4). */
    DENSE_RANK() OVER (
        ORDER BY total_spend DESC
    )   AS spend_rank,

    /* Calculates each customer's percentage share of global revenue */
    ROUND(
        total_spend * 100.0 /
            NULLIF(SUM(total_spend)
                OVER (), 0),
        2
    )   AS global_revenue_share_pct,

    /* Calculates each customer's percentage share of country-level revenue */
    ROUND(
        total_spend * 100.0 /
            NULLIF(SUM(total_spend)
                OVER(PARTITION BY country), 0),
        2
    )   AS country_revenue_share_pct

FROM customer_base;