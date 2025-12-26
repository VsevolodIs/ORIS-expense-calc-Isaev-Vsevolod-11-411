from flask import Flask, render_template, request, redirect, url_for, flash
from db import init_db, add_expense, get_expenses, get_stats, get_total

app = Flask(__name__)
app.secret_key = 'supersecretkey123'


@app.route('/', methods=['GET', 'POST'])
def index():
    init_db()

    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        add_expense(category, amount)
        flash('Расход добавлен', 'success')
        return redirect(url_for('index'))

    expenses = get_expenses(5)
    total = get_total()
    return render_template('index.html', expenses=expenses, total=total)


@app.route('/stats')
def stats():
    categories = get_stats()
    total = get_total()
    return render_template('stats.html', categories=categories, total=total)


@app.route('/clear')
def clear():
    import os
    os.remove('expenses.db')
    init_db()
    flash('Данные очищены', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)