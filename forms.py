from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateTimeField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password1 = PasswordField('Пароль (не менее пяти символов)', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class PerformanceForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    time = DateTimeField('Время начала (в формате ДД.ММ.ГГГГ ЧЧ:ММ)', validators=[DataRequired()],
                         format='%d.%m.%Y %H:%M')
    actors = TextAreaField('Актёры', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class ActorForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    role = StringField('*Тип* актёра', validators=[DataRequired()])
    bio = TextAreaField('Биография', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
