import os
import secrets

from PIL import Image
from flask import render_template, url_for, redirect, flash, request, abort
from flaskblog import app, bcrypt, db, mail
from flaskblog.forms import RegistrationForm, LoginForm, AccountUpdateForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Аккаунт  создан {form.username.data}! Вы можете войти в свой аккаунт!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Не правильный email или пароль', 'danger')
    return render_template('login.html', form=form, title='Войти')


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



@app.route('/account/<username>',  methods=['GET', 'POST'])
@login_required
def account(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = save_avatar(form.avatar.data)
            current_user.avatar = avatar_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Данные пользователя были обновлены!', 'success')
        return redirect(url_for('account', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    avatar = url_for('static', filename='profile_images/' + current_user.avatar)
    return render_template('account.html', form=form, avatar=avatar, user=user, title='Профиль')



@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Пост был создан!', 'success')
        redirect(url_for('index'))
    return render_template('create_post.html', form=form, title='Создать пост', legend='Создать пост')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Пост был обновлен!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', form=form, title='Изменить пост', legend='Изменить пост')



@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Пост был удален!', 'success')
    return redirect(url_for('index'))


@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc()).\
        paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user)

def send_reset_mail(user):
    token = user.get_reset_token()
    msg = Message('Сброс пароля', recipients=[user.email])
    msg.body = f'''Для того чтобы сбросить пароль перейдите по ссылке: 
    {url_for('reset_token', token=token, _external=True)} 
    Если вы не отправляли этот запрос, просто проигнорируйте это письмо, и никаких изменений не будет'''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_mail(user)
    return render_template('reset_request.html', title='Сброс пароля', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_token_reset(token)
    if user is None:
        flash('Это недействительный или просроченный токен', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль был обновлен! Теперь вы можете войти в систему', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Сброс пароля', form=form)
