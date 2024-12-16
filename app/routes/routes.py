from app import app
from flask import render_template, request, redirect, url_for, flash, session

app.secret_key = 'super_secret_key'  # Klucz dla sesji

# Strona główna
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Strona logowania
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "admin" and password == "password":
            session['username'] = username  # Ustawienie sesji
            flash("Zalogowano pomyślnie!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Nieprawidłowa nazwa użytkownika lub hasło", "danger")
    return render_template('login.html')

# Strona rejestracji
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        flash(f"Użytkownik {username} został pomyślnie zarejestrowany!", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

# Dashboard (dla zalogowanego użytkownika)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

# Wylogowanie
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Wylogowano pomyślnie.", "info")
    return redirect(url_for('login'))