from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import app, db
from app.models.expense import Expense
from app.models.category import Category
from sqlalchemy import func

# Dodawanie nowej kategorii
@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        new_category = Category(name=category_name, user_id=current_user.id)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('dashboard'))
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories.html', categories=categories)

# Dodawanie wydatków
@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        amount = float(request.form['amount'])
        description = request.form['description']
        category_id = request.form['category']
        new_expense = Expense(
            amount=amount,
            description=description,
            user_id=current_user.id,
            category_id=category_id
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('expenses.html', categories=categories)

# Dashboard - podsumowanie wydatków
@app.route('/dashboard')
@login_required
def dashboard():
    summary = db.session.query(
        Category.name.label('category'),
        func.MONTH(Expense.date).label('month'),
        func.YEAR(Expense.date).label('year'),
        func.sum(Expense.amount).label('total')
    ).join(Expense).filter(Expense.user_id == current_user.id)\
     .group_by(Category.name, func.MONTH(Expense.date), func.YEAR(Expense.date)).all()
    return render_template('dashboard.html', summaries=summary)