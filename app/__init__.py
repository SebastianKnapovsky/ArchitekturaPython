from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Tworzenie instancji aplikacji
app = Flask(__name__)

# Konfiguracja aplikacji
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://DESKTOP-VG7207B\\SQLEXPRESS/ArchitekturaPython?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja rozszerzeń
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Importowanie modeli w odpowiedniej kolejności
from app.models.user import User
from app.models.category import Category
from app.models.expense import Expense

# Flask-Login: ładowanie użytkownika
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Importowanie tras
from app.routes import routes, expenses