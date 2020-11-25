from flask import render_template, url_for, redirect, flash
from flaskblog import app, brycpt, db
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User


posts = [
    {
        'author': 'Эзербаев Иса',
        'title': 'Python Dict',
        'content': 'First post content',
        'date_posted': 'November 4, 2020'
    },
    {
        'author': 'Эзербаев Иса',
        'title': 'Python Tuple',
        'content': 'First post content',
        'date_posted': 'November 4, 2020'
    },
]

@app.route('/')
def index():
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = brycpt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Аккаунт  создан {form.username.data}! Вы можете войти в свой аккаунт!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)