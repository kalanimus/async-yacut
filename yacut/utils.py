from __future__ import annotations

from random import choices
from string import ascii_letters, digits
from typing import Optional

from yacut.models import URLMap

DEFAULT_SHORT_ID_LENGTH: int = 6
ALLOWED_SYMBOLS: str = ascii_letters + digits


def get_unique_short_id(length: int = DEFAULT_SHORT_ID_LENGTH) -> str:
    """Generate a unique short ID that doesn't exist in the database."""
    max_attempts: int = 100
    for _ in range(max_attempts):
        short_id: str = ''.join(choices(ALLOWED_SYMBOLS, k=length))
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id
    raise RuntimeError(
        f'Could not generate a unique short ID in {max_attempts} attempts'
    )


def is_valid_custom_id(custom_id: str) -> bool:
    """Check if a custom short ID contains only allowed characters."""
    return all(c in ALLOWED_SYMBOLS for c in custom_id) and 1 <= len(custom_id) <= 16


def get_short_id_or_none(custom_id: Optional[str]) -> str:
    """Return a custom short ID if valid and available, otherwise generate one."""
    if custom_id:
        return custom_id
    return get_unique_short_id()
