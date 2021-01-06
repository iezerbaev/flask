from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


from confing import Config

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message = 'Для доступа к данной странице нужно сделать регистрацию или войти в свой аккаунт!'
login_manager.login_message_category = 'info'




from flaskblog import routes