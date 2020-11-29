import os
import secrets

from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from flaskblog import app, brycpt, db
from flaskblog.forms import RegistrationForm, LoginForm, AccountUpdateForm
from flaskblog.models import User
from flask_login import login_user, logout_user, current_user, login_required


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
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = brycpt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Аккаунт  создан {form.username.data}! Вы можете войти в свой аккаунт!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and brycpt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Не правильный email или пароль', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_avatar(avatar):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(avatar.filename)
    avatar_name = random_hex + f_ext
    avatar_path = os.path.join(app.root_path, 'static/profile_images', avatar_name)
    avatar_size = (125, 125)
    i = Image.open(avatar)
    i.thumbnail(avatar_size)
    i.save(avatar_path)
    return avatar_name


@app.route('/account',  methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = save_avatar(form.avatar.data)
            current_user.avatar = avatar_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Данные пользователя были обновлены!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    avatar = url_for('static', filename='profile_images/' + current_user.avatar)
    return render_template('account.html', form=form, avatar=avatar)