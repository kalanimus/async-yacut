import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from yacut import app, db
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.error_handlers import InvalidAPIUsage


INVALID_SHORT_ID_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)
DUPLICATED_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if not data.get('url'):
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')

    if custom_id not in (None, ''):
        custom_id_is_invalid = (
            not isinstance(custom_id, str)
            or re.fullmatch(r'[A-Za-z0-9]{1,16}', custom_id) is None
        )

        if custom_id_is_invalid:
            raise InvalidAPIUsage(INVALID_SHORT_ID_MESSAGE)

        custom_id_is_busy = (
            custom_id == 'files'
            or URLMap.query.filter_by(short=custom_id).first() is not None
        )

        if custom_id_is_busy:
            raise InvalidAPIUsage(DUPLICATED_SHORT_ID_MESSAGE)

    short_id = custom_id or get_unique_short_id()

    url_map = URLMap(
        original=data['url'],
        short=short_id,
    )
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            'redirect_view',
            short_id=url_map.short,
            _external=True,
        ),
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()

    if url_map is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND,
        )

    return jsonify(url=url_map.original), HTTPStatus.OK