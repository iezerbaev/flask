from flaskblog import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    #avatar = db.Column(db.String(20), nullable=False, default='dafault.jpg')
    password = db.Column(db.String(20), nullable=False)