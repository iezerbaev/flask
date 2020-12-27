from flask_mail import Mail, Message
from flask import Flask
from config import *

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = email_username
app.config['MAIL_DEFAULT_SENDER'] = email_username
app.config['MAIL_PASSWORD'] = email_password


mail = Mail(app)

@app.route('/')
def index():
    msg = Message('Some text', recipients=['test@mail.ru'])
    mail.send(msg)
    return 'Hello!'

if __name__ == "__main__":
    app.run(debug=True)