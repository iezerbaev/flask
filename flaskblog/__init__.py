from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ff27c42a75864f7b443269bde9c3fef9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'email_username'
app.config['MAIL_DEFAULT_SENDER'] = 'email_username'
app.config['MAIL_PASSWORD'] = 'email_password'

mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message = 'Для доступа к данной странице нужно сделать регистрацию или войти в свой аккаунт!'
login_manager.login_message_category = 'info'




from flaskblog import routes