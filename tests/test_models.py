"""Tests for the URLMap model."""
from __future__ import annotations

from sqlalchemy import inspect

from yacut.models import URLMap
from tests.conftest import PY_URL


def test_model_fields(_app):
    """Verify all required fields exist on URLMap model."""
    inspector = inspect(URLMap)
    fields: list[str] = [column.name for column in inspector.columns]
    required = {'id', 'original', 'short', 'timestamp'}
    assert required.issubset(set(fields)), (
        f'URLMap model missing fields. Expected at least {required}, '
        f'got {set(fields)}'
    )


def test_model_creation(_app):
    """Test creating a URLMap instance and saving to DB."""
    url_map = URLMap(original=PY_URL, short='gh')
    from yacut import db
    db.session.add(url_map)
    db.session.commit()

    saved = URLMap.query.filter_by(short='gh').first()
    assert saved is not None
    assert saved.original == PY_URL
    assert saved.short == 'gh'
    assert saved.timestamp is not None


def test_model_unique_short_constraint(_app):
    """Test that duplicate short IDs are rejected at DB level."""
    from yacut import db

    url_map1 = URLMap(original=PY_URL, short='dup')
    db.session.add(url_map1)
    db.session.commit()

    from sqlalchemy.exc import IntegrityError
    url_map2 = URLMap(original='https://example.com', short='dup')
    db.session.add(url_map2)
    import pytest
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


def test_model_repr(_app):
    """Test the __repr__ method of URLMap."""
    url_map = URLMap(original=PY_URL, short='rp')
    from yacut import db
    db.session.add(url_map)
    db.session.commit()
    assert repr(url_map).startswith('<URLMap')
    assert 'rp' in repr(url_map)
    assert 'python.org' in repr(url_map)
