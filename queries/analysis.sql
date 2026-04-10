-- ============================================================
--  SQL SALES ANALYSIS — ALL QUERIES
--  Database: sales.db
--  Tables  : customers, products, orders
-- ============================================================


-- ────────────────────────────────────────────────────────────
-- QUERY 1: Total revenue, total orders, average order value
-- (Basic aggregation — the simplest starting point)
-- ────────────────────────────────────────────────────────────
SELECT
    COUNT(order_id)       AS total_orders,
    ROUND(SUM(revenue),2) AS total_revenue,
    ROUND(AVG(revenue),2) AS avg_order_value
FROM orders;


-- ────────────────────────────────────────────────────────────
-- QUERY 2: Revenue by category
-- (GROUP BY — most common interview question)
-- ────────────────────────────────────────────────────────────
SELECT
    p.category,
    COUNT(o.order_id)       AS total_orders,
    ROUND(SUM(o.revenue),2) AS total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- ────────────────────────────────────────────────────────────
-- QUERY 3: Top 5 best-selling products
-- (ORDER BY + LIMIT — filtering top results)
-- ────────────────────────────────────────────────────────────
SELECT
    p.product_name,
    p.category,
    COUNT(o.order_id)       AS times_ordered,
    ROUND(SUM(o.revenue),2) AS total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 5;


-- ────────────────────────────────────────────────────────────
-- QUERY 4: Monthly revenue trend
-- (Date functions — shows time-based thinking)
-- ────────────────────────────────────────────────────────────
SELECT
    STRFTIME('%Y-%m', order_date) AS month,
    COUNT(order_id)               AS total_orders,
    ROUND(SUM(revenue),2)         AS monthly_revenue
FROM orders
GROUP BY month
ORDER BY month;


-- ────────────────────────────────────────────────────────────
-- QUERY 5: Revenue by city
-- (Multi-table JOIN — joining 3 tables)
-- ────────────────────────────────────────────────────────────
SELECT
    c.city,
    COUNT(o.order_id)       AS total_orders,
    ROUND(SUM(o.revenue),2) AS total_revenue,
    ROUND(AVG(o.revenue),2) AS avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY total_revenue DESC;


-- ────────────────────────────────────────────────────────────
-- QUERY 6: Return rate by category
-- (CASE WHEN inside aggregation — conditional logic)
-- ────────────────────────────────────────────────────────────
SELECT
    p.category,
    COUNT(o.order_id)                                    AS total_orders,
    SUM(o.returned)                                      AS total_returns,
    ROUND(SUM(o.returned) * 100.0 / COUNT(o.order_id),1) AS return_rate_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY return_rate_pct DESC;


-- ────────────────────────────────────────────────────────────
-- QUERY 7: Top 10 customers by revenue
-- (Subquery — finding high-value customers)
-- ────────────────────────────────────────────────────────────
SELECT
    c.customer_name,
    c.city,
    COUNT(o.order_id)       AS total_orders,
    ROUND(SUM(o.revenue),2) AS total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_spent DESC
LIMIT 10;


-- ────────────────────────────────────────────────────────────
-- QUERY 8: Running total of revenue by month
-- (Window function — cumulative sum over time)
-- ────────────────────────────────────────────────────────────
WITH monthly AS (
    SELECT
        STRFTIME('%Y-%m', order_date) AS month,
        ROUND(SUM(revenue),2)         AS monthly_revenue
    FROM orders
    GROUP BY month
)
SELECT
    month,
    monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (ORDER BY month), 2) AS running_total
FROM monthly
ORDER BY month;


-- ────────────────────────────────────────────────────────────
-- QUERY 9: Rank products by revenue within each category
-- (Window function — RANK() OVER PARTITION BY)
-- ────────────────────────────────────────────────────────────
WITH product_revenue AS (
    SELECT
        p.category,
        p.product_name,
        ROUND(SUM(o.revenue),2) AS total_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category, p.product_name
)
SELECT
    category,
    product_name,
    total_revenue,
    RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category
FROM product_revenue
ORDER BY category, rank_in_category;


-- ────────────────────────────────────────────────────────────
-- QUERY 10: Month-over-month revenue growth
-- (Window function — LAG to compare with previous month)
-- ────────────────────────────────────────────────────────────
WITH monthly AS (
    SELECT
        STRFTIME('%Y-%m', order_date) AS month,
        ROUND(SUM(revenue),2)         AS monthly_revenue
    FROM orders
    GROUP BY month
)
SELECT
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month)  AS prev_month_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month))
        * 100.0
        / LAG(monthly_revenue) OVER (ORDER BY month),
    1) AS growth_pct
FROM monthly
ORDER BY month;


-- ────────────────────────────────────────────────────────────
-- QUERY 11: Customers who ordered more than average
-- (Subquery in WHERE clause)
-- ────────────────────────────────────────────────────────────
SELECT
    c.customer_name,
    c.city,
    COUNT(o.order_id)       AS total_orders,
    ROUND(SUM(o.revenue),2) AS total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
HAVING total_orders > (
    SELECT AVG(order_count)
    FROM (
        SELECT COUNT(order_id) AS order_count
        FROM orders
        GROUP BY customer_id
    )
)
ORDER BY total_orders DESC;


-- ────────────────────────────────────────────────────────────
-- QUERY 12: Best month for each category
-- (CTE + Window function combined)
-- ────────────────────────────────────────────────────────────
WITH monthly_cat AS (
    SELECT
        p.category,
        STRFTIME('%Y-%m', o.order_date) AS month,
        ROUND(SUM(o.revenue),2)         AS revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category, month
),
ranked AS (
    SELECT *,
        RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
    FROM monthly_cat
)
SELECT category, month AS best_month, revenue AS peak_revenue
FROM ranked
WHERE rnk = 1
ORDER BY peak_revenue DESC;
