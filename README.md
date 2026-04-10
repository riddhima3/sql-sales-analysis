# 🗄️ SQL Sales Analysis

A beginner-friendly SQL project that answers real business questions using a SQLite database with 3 tables and 2,000 orders.

---

## 📁 Project Structure

```
sql-sales-analysis/
├── data/
│   ├── sales.db              ← SQLite database
│   └── setup_database.py     ← Script to recreate the DB
├── queries/
│   └── analysis.sql          ← All 12 SQL queries (plain SQL file)
├── notebooks/
│   └── sql_analysis.ipynb    ← Jupyter notebook with explanations
├── outputs/
│   ├── 01_category_revenue.png
│   ├── 02_monthly_trend.png
│   ├── 03_city_revenue.png
│   ├── 04_running_total.png
│   ├── 05_mom_growth.png
│   └── *.csv                 ← Query results exported as CSV
├── run_analysis.py           ← Runs all queries + saves charts
└── requirements.txt
```

---

## 🗃️ Database Schema

**customers**
| Column | Type |
|--------|------|
| customer_id | INTEGER |
| customer_name | TEXT |
| city | TEXT |
| signup_date | TEXT |

**products**
| Column | Type |
|--------|------|
| product_id | INTEGER |
| product_name | TEXT |
| category | TEXT |
| unit_price | REAL |

**orders**
| Column | Type |
|--------|------|
| order_id | INTEGER |
| customer_id | INTEGER (FK) |
| product_id | INTEGER (FK) |
| order_date | TEXT |
| quantity | INTEGER |
| discount | REAL |
| revenue | REAL |
| returned | INTEGER (0/1) |

---

## 🔍 Queries Covered

| # | Business Question | SQL Concept |
|---|------------------|-------------|
| 1 | Total revenue, orders, avg order value | Basic aggregation |
| 2 | Revenue by category | GROUP BY + JOIN |
| 3 | Top 5 products | ORDER BY + LIMIT |
| 4 | Monthly revenue trend | Date functions |
| 5 | Revenue by city | 3-table JOIN |
| 6 | Return rate by category | Division in aggregation |
| 7 | Top 10 customers | JOIN + GROUP BY |
| 8 | Running total revenue | Window: SUM() OVER |
| 9 | Product rank within category | Window: RANK() OVER PARTITION BY |
| 10 | Month-over-month growth | Window: LAG() |
| 11 | Customers above average orders | Subquery in HAVING |
| 12 | Best month per category | CTE + Window combined |

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/sql-sales-analysis.git
cd sql-sales-analysis

# Install dependencies
pip install -r requirements.txt

# Step 1 — Create the database
python data/setup_database.py

# Step 2 — Run all queries
python run_analysis.py

# Step 3 — Or open the notebook
jupyter notebook notebooks/sql_analysis.ipynb
```

---

## 📊 Key Insights

- Electronics accounts for **~77% of total revenue**
- **Laptop** is the single best-selling product
- **Hyderabad** is the top revenue city
- **May & June** are the strongest months
- **Books** have the highest return rate (15.4%)
- Cumulative revenue reached **₹4.65 Lakhs** by year end

---

## 🛠 Tech Stack

- **SQLite** — lightweight SQL database, no setup needed
- **Python + pandas** — run queries and analyse results
- **Matplotlib + Seaborn** — visualise query outputs
- **Jupyter Notebook** — interactive walkthrough
