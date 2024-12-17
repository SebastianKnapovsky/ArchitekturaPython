from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Klucz potrzebny do flashowania komunikatów i sesji

# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc://@DESKTOP-VG7207B\\SQLEXPRESS/ArchitekturaPython"
    "?trusted_connection=yes"
    "&driver=ODBC+Driver+17+for+SQL+Server"
    "&TrustServerCertificate=yes"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja rozszerzeń
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))

# Importowanie tras
from app.routes import routes