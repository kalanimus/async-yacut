from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import FileForm, URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.yandex_disk import upload_files

DUPLICATED_SHORT_ID_MESSAGE: str = (
    'Предложенный вариант короткой ссылки уже существует.'
)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form: URLMapForm = URLMapForm()
    short_url: str | None = None

    if form.validate_on_submit():
        custom_id: str | None = (form.custom_id.data or '').strip() or None

        short_id_is_busy: bool = (
            custom_id == 'files'
            or (
                custom_id is not None
                and URLMap.query.filter_by(short=custom_id).first() is not None
            )
        )

        if short_id_is_busy:
            flash(DUPLICATED_SHORT_ID_MESSAGE)
            return render_template('index.html', form=form)

        short_id: str = custom_id or get_unique_short_id()

        url_map: URLMap = URLMap(
            original=form.original_link.data,
            short=short_id,
        )
        db.session.add(url_map)
        db.session.commit()

        short_url = url_for(
            'redirect_view',
            short_id=short_id,
            _external=True,
        )

    return render_template(
        'index.html',
        form=form,
        short_url=short_url,
    )


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form: FileForm = FileForm()
    uploaded_files: list[dict[str, Any]] = []

    if form.validate_on_submit():
        disk_files: list[tuple[str, str]] = await upload_files(
            form.files.data,
            app.config['DISK_TOKEN'],
        )

        for filename, download_url in disk_files:
            short_id: str = get_unique_short_id()

            url_map: URLMap = URLMap(
                original=download_url,
                short=short_id,
            )
            db.session.add(url_map)

            uploaded_files.append({
                'filename': filename,
                'short_url': url_for(
                    'redirect_view',
                    short_id=short_id,
                    _external=True,
                ),
            })

        db.session.commit()

    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files,
    )


@app.route('/<string:short_id>')
def redirect_view(short_id: str):
    url_map: URLMap = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
