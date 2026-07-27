from __future__ import annotations

import re
from http import HTTPStatus
from typing import Any

from flask import jsonify, request, url_for

from yacut import app, db
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.error_handlers import InvalidAPIUsage

INVALID_SHORT_ID_MESSAGE: str = (
    'Указано недопустимое имя для короткой ссылки'
)
DUPLICATED_SHORT_ID_MESSAGE: str = (
    'Предложенный вариант короткой ссылки уже существует.'
)
URL_REQUIRED_MESSAGE: str = (
    '"url" является обязательным полем!'
)
BODY_MISSING_MESSAGE: str = (
    'Отсутствует тело запроса'
)
ID_NOT_FOUND_MESSAGE: str = (
    'Указанный id не найден'
)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data: Any | None = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage(BODY_MISSING_MESSAGE)

    url: str | None = data.get('url')
    if not url:
        raise InvalidAPIUsage(URL_REQUIRED_MESSAGE)

    custom_id: str | None = data.get('custom_id')

    if custom_id:
        if not isinstance(custom_id, str) or not re.fullmatch(
            r'[A-Za-z0-9]{1,16}', custom_id
        ):
            raise InvalidAPIUsage(INVALID_SHORT_ID_MESSAGE)

        if custom_id == 'files' or URLMap.query.filter_by(
            short=custom_id
        ).first() is not None:
            raise InvalidAPIUsage(DUPLICATED_SHORT_ID_MESSAGE)

    short_id: str = custom_id or get_unique_short_id()

    url_map: URLMap = URLMap(
        original=url,
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
def get_original_link(short_id: str):
    url_map: URLMap | None = URLMap.query.filter_by(short=short_id).first()

    if url_map is None:
        raise InvalidAPIUsage(
            ID_NOT_FOUND_MESSAGE,
            HTTPStatus.NOT_FOUND,
        )

    return jsonify(url=url_map.original), HTTPStatus.OK
