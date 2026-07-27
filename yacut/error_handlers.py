from __future__ import annotations

from http import HTTPStatus

from flask import jsonify, render_template

from yacut import app, db


class InvalidAPIUsage(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = HTTPStatus.BAD_REQUEST,
    ) -> None:
        super().__init__(message)
        self.message: str = message
        self.status_code: int = status_code


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_api_usage(error: InvalidAPIUsage):
    return jsonify(message=error.message), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error: Exception):
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error: Exception):
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
