"""Tests for utility functions."""
from __future__ import annotations

import pytest

from yacut.utils import (
    get_unique_short_id,
    is_valid_custom_id,
    get_short_id_or_none,
    DEFAULT_SHORT_ID_LENGTH,
)


class TestGetUniqueShortId:
    def test_default_length(self, _app):
        """Generated short ID should have default length."""
        short_id: str = get_unique_short_id()
        assert len(short_id) == DEFAULT_SHORT_ID_LENGTH

    def test_custom_length(self, _app):
        """Generated short ID should respect custom length."""
        short_id: str = get_unique_short_id(length=10)
        assert len(short_id) == 10

    def test_contains_only_allowed_chars(self, _app):
        """Generated short ID should only contain alphanumeric chars."""
        short_id: str = get_unique_short_id()
        assert short_id.isalnum()

    def test_is_unique(self, _app):
        """Generated short IDs should be unique."""
        ids: set[str] = set()
        for _ in range(100):
            ids.add(get_unique_short_id(length=8))
        assert len(ids) == 100


class TestIsValidCustomId:
    def test_valid_simple(self):
        assert is_valid_custom_id('abc123')

    def test_valid_uppercase(self):
        assert is_valid_custom_id('ABC')

    def test_invalid_special_chars(self):
        assert not is_valid_custom_id('hello!')

    def test_invalid_unicode(self):
        assert not is_valid_custom_id('привет')

    def test_invalid_hyphen(self):
        assert not is_valid_custom_id('test-id')

    def test_invalid_too_long(self):
        long_id = 'a' * 17
        assert not is_valid_custom_id(long_id)

    def test_invalid_empty(self):
        assert not is_valid_custom_id('')


class TestGetShortIdOrNone:
    def test_returns_custom_id_when_provided(self):
        assert get_short_id_or_none('custom') == 'custom'

    def test_returns_new_id_when_none(self, _app):
        short_id: str = get_short_id_or_none(None)
        assert len(short_id) == DEFAULT_SHORT_ID_LENGTH

    def test_returns_new_id_when_empty(self, _app):
        short_id: str = get_short_id_or_none('')
        assert len(short_id) == DEFAULT_SHORT_ID_LENGTH
