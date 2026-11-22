from datetime import datetime
from random import choice

from flask import url_for

from yacut import db
from yacut.constants import (
    ALLOWED_CHARS,
    AUTO_SHORT_ID_LENGTH,
    MAX_LENGTH_SHORT_ID,
    MAX_SHORT_ID_ATTEMPTS,
    RESERVED_SHORT_IDS,
)
from yacut.error_handlers import ShortIdGenerationError


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(MAX_LENGTH_SHORT_ID),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(
        db.DateTime, index=True, default=datetime.utcnow
    )

    def get_absolute_url(self):
        """Возвращает абсолютный URL для короткой ссылки."""
        return url_for(
            'redirect_view', short_id=self.short, _external=True
        )

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': self.get_absolute_url()
        }

    @classmethod
    def get(cls, short_id):
        """Возвращает объект по короткому ID или None."""
        return cls.query.filter_by(short=short_id).first()

    @classmethod
    def create(cls, original, custom_id=None):
        """Микро-ORM для создания новой записи."""
        if custom_id:
            if custom_id in RESERVED_SHORT_IDS or cls.get(custom_id):
                error_msg = (
                    'Предложенный вариант короткой ссылки уже существует.'
                )
                raise ValueError(error_msg)
            short_id = custom_id
        else:
            short_id = cls.get_unique_short_id()

        url_map = cls(original=original, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @classmethod
    def get_unique_short_id(cls):
        """Генерирует уникальный ID с ограничением попыток."""
        for _ in range(MAX_SHORT_ID_ATTEMPTS):
            short_id = ''.join(
                choice(ALLOWED_CHARS)
                for _ in range(AUTO_SHORT_ID_LENGTH)
            )
            if not cls.get(short_id):
                return short_id
        raise ShortIdGenerationError(
            'Не удалось сгенерировать уникальный ID'
        )
