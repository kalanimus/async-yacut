from __future__ import annotations

from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL


class URLMapForm(FlaskForm):
    original_link: StringField = StringField(
        'Original URL',
        validators=[
            DataRequired(message='This field is required'),
            URL(message='Enter a valid URL'),
        ],
    )
    custom_id: StringField = StringField(
        'Custom short URL (optional)',
        validators=[
            Optional(),
            Length(
                max=16,
                message='Short URL must not exceed 16 characters',
            ),
            Regexp(
                r'^[A-Za-z0-9]+$',
                message='Only Latin letters and digits are allowed',
            ),
        ],
    )
    submit: SubmitField = SubmitField('Create')


class FileForm(FlaskForm):
    files: MultipleFileField = MultipleFileField(
        'Select files',
        validators=[DataRequired(message='Select at least one file')],
    )
    submit: SubmitField = SubmitField('Upload')
