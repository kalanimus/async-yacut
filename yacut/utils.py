from random import choices
from string import ascii_letters, digits

from yacut import app
from yacut.models import URLMap


DEFAULT_SHORT_ID_LENGTH = 6
ALLOWED_SYMBOLS = ascii_letters + digits


def is_reserved_short_id(short_id):
    if not short_id:
        return False

    return any(
        not rule.arguments
        and rule.rule.strip('/') == short_id
        for rule in app.url_map.iter_rules()
    )


def get_unique_short_id(length=DEFAULT_SHORT_ID_LENGTH):
    while True:
        short_id = ''.join(choices(ALLOWED_SYMBOLS, k=length))
        if (
            not is_reserved_short_id(short_id)
            and URLMap.query.filter_by(short=short_id).first() is None
        ):
            return short_id