from random import choices
from string import ascii_letters, digits

from yacut.models import URLMap


DEFAULT_SHORT_ID_LENGTH = 6
ALLOWED_SYMBOLS = ascii_letters + digits


def get_unique_short_id(length=DEFAULT_SHORT_ID_LENGTH):
    while True:
        short_id = ''.join(choices(ALLOWED_SYMBOLS, k=length))
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id