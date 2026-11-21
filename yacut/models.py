from datetime import datetime
from random import choice
from string import ascii_letters, digits

from yacut import db

MAX_LENGTH_SHORT_ID = 16
AUTO_SHORT_ID_LENGTH = 6
ALLOWED_CHARS = ascii_letters + digits


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(MAX_LENGTH_SHORT_ID),
        unique=True,
        nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_unique_short_id():
        """Генерирует уникальный короткий ID."""
        while True:
            short_id = "".join(
                choice(ALLOWED_CHARS) for _ in range(AUTO_SHORT_ID_LENGTH)
            )
            if not URLMap.query.filter_by(short=short_id).first():
                return short_id
