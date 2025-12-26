import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(category, amount):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)',
        (category, amount, datetime.now().strftime('%d.%m.%Y %H:%M'))
    )
    conn.commit()
    conn.close()

def get_expenses(limit=5):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, category, amount, date FROM expenses '
        'ORDER BY id DESC LIMIT ?',
        (limit,)
    )

    expenses = []
    for row in cursor.fetchall():
        expense = {
            'id': row[0],
            'category': row[1],
            'amount': row[2],
            'date': row[3],
        }
        expenses.append(expense)

    conn.close()
    return expenses

def get_stats():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    sql = 'SELECT category, SUM(amount) FROM expenses GROUP BY category'
    cursor.execute(sql)

    categories = {}
    rows = cursor.fetchall()
    for row in rows:
        category = row[0]
        amount = row[1]
        categories[category] = amount

    conn.close()
    return categories

def get_total():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    sql = 'SELECT SUM(amount) FROM expenses'
    cursor.execute(sql)

    row = cursor.fetchone()
    if row is None or row[0] is None:
        total = 0
    else:
        total = row[0]

    conn.close()
    return total