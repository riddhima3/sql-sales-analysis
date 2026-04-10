import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# ── Create database ────────────────────────────────────────────────
conn = sqlite3.connect('data/sales.db')
cursor = conn.cursor()

# ── Create tables ──────────────────────────────────────────────────
cursor.executescript('''
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    customer_name TEXT,
    city          TEXT,
    signup_date   TEXT
);

CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT,
    category     TEXT,
    unit_price   REAL
);

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id  INTEGER,
    order_date  TEXT,
    quantity    INTEGER,
    discount    REAL,
    revenue     REAL,
    returned    INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
);
''')

# ── Seed data ──────────────────────────────────────────────────────
cities    = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune']
firstnames = ['Amit', 'Priya', 'Rahul', 'Sneha', 'Vikram', 'Neha', 'Rohan', 'Anjali', 'Karan', 'Pooja',
              'Arjun', 'Divya', 'Suresh', 'Meena', 'Ravi', 'Sonal', 'Nikhil', 'Kavya', 'Arun', 'Simran']
lastnames  = ['Sharma', 'Patel', 'Singh', 'Kumar', 'Mehta', 'Joshi', 'Nair', 'Iyer', 'Gupta', 'Verma']

customers = []
for i in range(1, 201):
    name = f"{random.choice(firstnames)} {random.choice(lastnames)}"
    city = random.choice(cities)
    days_ago = random.randint(30, 730)
    signup = (datetime(2023, 1, 1) - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    customers.append((i, name, city, signup))

cursor.executemany('INSERT INTO customers VALUES (?,?,?,?)', customers)

product_data = [
    (1,  'Laptop',        'Electronics',    899.99),
    (2,  'Smartphone',    'Electronics',    599.99),
    (3,  'Headphones',    'Electronics',    149.99),
    (4,  'Tablet',        'Electronics',    399.99),
    (5,  'Smartwatch',    'Electronics',    249.99),
    (6,  'T-Shirt',       'Clothing',        29.99),
    (7,  'Jeans',         'Clothing',        59.99),
    (8,  'Jacket',        'Clothing',        89.99),
    (9,  'Sneakers',      'Clothing',        79.99),
    (10, 'Blender',       'Home & Kitchen',  49.99),
    (11, 'Air Fryer',     'Home & Kitchen',  89.99),
    (12, 'Coffee Maker',  'Home & Kitchen',  69.99),
    (13, 'Yoga Mat',      'Sports',          29.99),
    (14, 'Dumbbells',     'Sports',          49.99),
    (15, 'Face Cream',    'Beauty',          19.99),
    (16, 'Perfume',       'Beauty',          59.99),
    (17, 'Fiction Novel', 'Books',           14.99),
    (18, 'Cookbook',      'Books',           24.99),
]
cursor.executemany('INSERT INTO products VALUES (?,?,?,?)', product_data)

orders = []
start = datetime(2023, 1, 1)
for i in range(1, 2001):
    cust_id   = random.randint(1, 200)
    prod_id   = random.randint(1, 18)
    price     = dict((p[0], p[3]) for p in product_data)[prod_id]
    qty       = random.choices([1,2,3], weights=[0.6,0.3,0.1])[0]
    discount  = random.choices([0, 0.05, 0.10, 0.15, 0.20], weights=[0.4,0.2,0.2,0.1,0.1])[0]
    revenue   = round(price * qty * (1 - discount), 2)
    date      = (start + timedelta(days=random.randint(0, 364))).strftime('%Y-%m-%d')
    returned  = random.choices([0, 1], weights=[0.88, 0.12])[0]
    orders.append((i, cust_id, prod_id, date, qty, discount, revenue, returned))

cursor.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?,?,?)', orders)
conn.commit()
conn.close()
print("Database created: data/sales.db")
print(f"  Customers : 200")
print(f"  Products  : 18")
print(f"  Orders    : 2,000")
