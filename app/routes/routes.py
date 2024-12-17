from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models.user import User

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            error = "Nieprawidłowa nazwa użytkownika lub hasło."

    return render_template('login.html', error=error)

# Rejestracja
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            error = "Nazwa użytkownika jest już zajęta."
        elif User.query.filter_by(email=email).first():
            error = "Adres e-mail jest już zarejestrowany."
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            success = "Rejestracja zakończona sukcesem. Możesz się teraz zalogować."
            return redirect(url_for('login'))

    return render_template('register.html', error=error, success=success)

# Wylogowanie
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))