from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from src.models import UserModel


class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[
        DataRequired(message="Имя пользователя обязательно"),
        Length(min=3, max=80, message="Длина (от 3 до 80 символов)")
    ])
    password = PasswordField("Пароль", validators=[
        DataRequired(message="Имя пользователя обязательно"),
        Length(min=6, max=32, message="Пароль (от 6 до 32 символов)")
    ])
    submit = SubmitField("Зарегистрироваться")

    def validate_username(self, field) -> None:
        if UserModel.query.filter_by(username=field.data).first(): raise ValidationError("Это имя пользователя уже занято")


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[
        DataRequired(message="Имя пользователя обязательно")
    ])
    password = PasswordField("Пароль", validators=[
        DataRequired(message="Пароль обязателен")
    ])
    submit = SubmitField("Войти")


class NoteForm(FlaskForm):
    title = StringField("Заголовок", validators=[
        DataRequired(message="Заголовок обязателен"),
        Length(max=200, message="Заголовок (не более 200 символов)")
    ])
    content = TextAreaField("Содержание", validators=[
        DataRequired(message="Содержание обязательно")
    ])
    submit = SubmitField("Сохранить")


class DeleteNoteForm(FlaskForm):
    submit = SubmitField("Удалить")

