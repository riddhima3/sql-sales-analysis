"""
SQL Sales Analysis — Run all queries and export results
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('outputs', exist_ok=True)

conn = sqlite3.connect('data/sales.db')
sns.set_theme(style='whitegrid', palette='muted')
COLORS = sns.color_palette('muted', 10)

print("=" * 55)
print("  SQL SALES ANALYSIS — QUERY RESULTS")
print("=" * 55)

# ── Q1: Overall summary ────────────────────────────────────────────
q1 = pd.read_sql("""
    SELECT
        COUNT(order_id)       AS total_orders,
        ROUND(SUM(revenue),2) AS total_revenue,
        ROUND(AVG(revenue),2) AS avg_order_value
    FROM orders
""", conn)
print("\n[Q1] Overall Summary")
print(q1.to_string(index=False))

# ── Q2: Revenue by category ────────────────────────────────────────
q2 = pd.read_sql("""
    SELECT p.category,
           COUNT(o.order_id)       AS total_orders,
           ROUND(SUM(o.revenue),2) AS total_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_revenue DESC
""", conn)
print("\n[Q2] Revenue by Category")
print(q2.to_string(index=False))

fig, ax = plt.subplots(figsize=(9,5))
ax.barh(q2['category'], q2['total_revenue'], color=COLORS[:len(q2)])
ax.set_xlabel('Total Revenue (₹)')
ax.set_title('Revenue by Category')
plt.tight_layout()
plt.savefig('outputs/01_category_revenue.png')
plt.close()

# ── Q3: Top 5 products ─────────────────────────────────────────────
q3 = pd.read_sql("""
    SELECT p.product_name, p.category,
           COUNT(o.order_id)       AS times_ordered,
           ROUND(SUM(o.revenue),2) AS total_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY total_revenue DESC
    LIMIT 5
""", conn)
print("\n[Q3] Top 5 Products")
print(q3.to_string(index=False))

# ── Q4: Monthly trend ──────────────────────────────────────────────
q4 = pd.read_sql("""
    SELECT STRFTIME('%Y-%m', order_date) AS month,
           COUNT(order_id)               AS total_orders,
           ROUND(SUM(revenue),2)         AS monthly_revenue
    FROM orders
    GROUP BY month
    ORDER BY month
""", conn)
print("\n[Q4] Monthly Revenue")
print(q4.to_string(index=False))

fig, ax = plt.subplots(figsize=(12,4))
ax.plot(q4['month'], q4['monthly_revenue'], marker='o', color=COLORS[0], linewidth=2)
ax.fill_between(q4['month'], q4['monthly_revenue'], alpha=0.15, color=COLORS[0])
ax.set_title('Monthly Revenue Trend')
ax.set_ylabel('Revenue (₹)')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('outputs/02_monthly_trend.png')
plt.close()

# ── Q5: City revenue ───────────────────────────────────────────────
q5 = pd.read_sql("""
    SELECT c.city,
           COUNT(o.order_id)       AS total_orders,
           ROUND(SUM(o.revenue),2) AS total_revenue
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.city
    ORDER BY total_revenue DESC
""", conn)
print("\n[Q5] Revenue by City")
print(q5.to_string(index=False))

fig, ax = plt.subplots(figsize=(9,5))
ax.bar(q5['city'], q5['total_revenue'], color=COLORS[2])
ax.set_title('Revenue by City')
ax.set_ylabel('Revenue (₹)')
plt.tight_layout()
plt.savefig('outputs/03_city_revenue.png')
plt.close()

# ── Q6: Return rate ────────────────────────────────────────────────
q6 = pd.read_sql("""
    SELECT p.category,
           ROUND(SUM(o.returned) * 100.0 / COUNT(o.order_id),1) AS return_rate_pct
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category
    ORDER BY return_rate_pct DESC
""", conn)
print("\n[Q6] Return Rate by Category")
print(q6.to_string(index=False))

# ── Q7: Top 10 customers ───────────────────────────────────────────
q7 = pd.read_sql("""
    SELECT c.customer_name, c.city,
           COUNT(o.order_id)       AS total_orders,
           ROUND(SUM(o.revenue),2) AS total_spent
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.customer_id
    ORDER BY total_spent DESC
    LIMIT 10
""", conn)
print("\n[Q7] Top 10 Customers")
print(q7.to_string(index=False))

# ── Q8: Running total ──────────────────────────────────────────────
q8 = pd.read_sql("""
    WITH monthly AS (
        SELECT STRFTIME('%Y-%m', order_date) AS month,
               ROUND(SUM(revenue),2)         AS monthly_revenue
        FROM orders GROUP BY month
    )
    SELECT month, monthly_revenue,
           ROUND(SUM(monthly_revenue) OVER (ORDER BY month),2) AS running_total
    FROM monthly ORDER BY month
""", conn)
print("\n[Q8] Running Total Revenue")
print(q8.to_string(index=False))

fig, ax = plt.subplots(figsize=(12,4))
ax.plot(q8['month'], q8['running_total'], marker='s', color=COLORS[3], linewidth=2)
ax.set_title('Cumulative Revenue — 2023')
ax.set_ylabel('Running Total (₹)')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('outputs/04_running_total.png')
plt.close()

# ── Q9: Product rank within category ──────────────────────────────
q9 = pd.read_sql("""
    WITH product_revenue AS (
        SELECT p.category, p.product_name,
               ROUND(SUM(o.revenue),2) AS total_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.category, p.product_name
    )
    SELECT category, product_name, total_revenue,
           RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category
    FROM product_revenue
    ORDER BY category, rank_in_category
""", conn)
print("\n[Q9] Product Rank Within Category")
print(q9.to_string(index=False))

# ── Q10: Month-over-month growth ───────────────────────────────────
q10 = pd.read_sql("""
    WITH monthly AS (
        SELECT STRFTIME('%Y-%m', order_date) AS month,
               ROUND(SUM(revenue),2)         AS monthly_revenue
        FROM orders GROUP BY month
    )
    SELECT month, monthly_revenue,
           LAG(monthly_revenue) OVER (ORDER BY month) AS prev_month,
           ROUND((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month))
                 * 100.0 / LAG(monthly_revenue) OVER (ORDER BY month), 1) AS growth_pct
    FROM monthly ORDER BY month
""", conn)
print("\n[Q10] Month-over-Month Growth")
print(q10.to_string(index=False))

fig, ax = plt.subplots(figsize=(12,4))
colors = [COLORS[1] if x >= 0 else COLORS[3] for x in q10['growth_pct'].fillna(0)]
ax.bar(q10['month'], q10['growth_pct'].fillna(0), color=colors)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title('Month-over-Month Revenue Growth (%)')
ax.set_ylabel('Growth %')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('outputs/05_mom_growth.png')
plt.close()

# ── Save all results to CSV ────────────────────────────────────────
q2.to_csv('outputs/category_revenue.csv', index=False)
q4.to_csv('outputs/monthly_revenue.csv', index=False)
q5.to_csv('outputs/city_revenue.csv', index=False)
q7.to_csv('outputs/top_customers.csv', index=False)
q10.to_csv('outputs/mom_growth.csv', index=False)

conn.close()
print("\n" + "="*55)
print("  Done! Charts + CSVs saved to outputs/")
print("="*55)
