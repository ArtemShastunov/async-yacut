from http import HTTPStatus

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.forms import URLMapForm
from yacut.models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id:
        form = URLMapForm(
            data={'original_link': data['url'], 'custom_id': custom_id},
            meta={'csrf': False}
        )
        if not form.validate():
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        if (
            custom_id == 'files'
            or URLMap.query.filter_by(short=custom_id).first()
        ):
            error_msg = 'Предложенный вариант короткой ссылки уже существует.'
            raise InvalidAPIUsage(error_msg)
    else:
        custom_id = URLMap.get_unique_short_id()

    url_map = URLMap(original=data['url'], short=custom_id)
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': f'{request.host_url}{url_map.short}'
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': url_map.original}), HTTPStatus.OK
