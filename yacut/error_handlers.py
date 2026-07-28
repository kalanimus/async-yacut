from http import HTTPStatus

from flask import jsonify, render_template

from yacut import app, db


class InvalidAPIUsage(Exception):
    def __init__(
        self,
        message,
        status_code=HTTPStatus.BAD_REQUEST,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_api_usage(error):
    return jsonify(
        message=error.message
    ), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        '404.html'
    ), HTTPStatus.NOT_FOUND


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template(
        '500.html'
    ), HTTPStatus.INTERNAL_SERVER_ERROR