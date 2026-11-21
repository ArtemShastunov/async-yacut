from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from yacut.models import MAX_LENGTH_SHORT_ID


class URLMapForm(FlaskForm):
    original_link = URLField(
        "Длинная ссылка",
        validators=[
            DataRequired(
                message="Обязательное поле"),
            URL()])
    custom_id = StringField(
        "Ваш вариант короткой ссылки",
        validators=[
            Length(max=MAX_LENGTH_SHORT_ID, message="Слишком длинный ID"),
            Regexp(
                regex=r"^[a-zA-Z0-9]+$",
                message="Укажите только латинские буквы и цифры",
            ),
            Optional(),
        ],
    )
    submit = SubmitField("Создать")


class FileUploadForm(FlaskForm):
    files = FileField(
        "Выберите файлы", validators=[FileRequired(message="Файл не выбран")]
    )
    submit = SubmitField("Загрузить")
