from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator
from flaskblog.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(message="Это поле не может быть пустым!"), Length(min=2, max=20, message="Длина")])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    confirm_password = PasswordField("Потверждение пароля", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Регистрация")


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такой логин существует!')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Такой email существует!')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить")
    submit = SubmitField("Войти")



class AccountUpdateForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(message="Это поле не может быть пустым!"), Length(min=2, max=20, message="Длина")])
    email = StringField("Email", validators=[DataRequired(), Email()])
    avatar = FileField('Фото профиля', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Обновить")


    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Такой логин существует!')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Такой email существует!')



class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Контент', validators=[DataRequired()])
    submit = SubmitField('Создать пост')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Cброс пароля')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Нет учетной записи с этим адресом электронной почты. Вы должны сначала зарегистрироваться.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Потверждение пароля',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сброс пароля')