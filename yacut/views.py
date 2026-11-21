from http import HTTPStatus

from flask import flash, redirect, render_template, request

from yacut import app, db
from yacut.disk import upload_files_to_disk
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = URLMap.get_unique_short_id()
        elif (
            custom_id == 'files'
            or URLMap.query.filter_by(short=custom_id).first()
        ):
            error_msg = 'Предложенный вариант короткой ссылки уже существует.'
            flash(error_msg)
            return render_template('index.html', form=form)

        url_map = URLMap(
            original=form.original_link.data, short=custom_id
        )
        db.session.add(url_map)
        db.session.commit()

        return render_template(
            'index.html',
            form=form,
            short_link=f'{request.host_url}{url_map.short}'
        )
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileUploadForm()
    if form.validate_on_submit():
        files = request.files.getlist('files')

        uploaded_files = await upload_files_to_disk(files)

        results = []
        for filename, original_url in uploaded_files:
            short_id = URLMap.get_unique_short_id()
            url_map = URLMap(original=original_url, short=short_id)
            db.session.add(url_map)
            db.session.commit()

            results.append({
                'filename': filename,
                'short_link': f'{request.host_url}{short_id}'
            })

        return render_template('files.html', form=form, results=results)

    return render_template('files.html', form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        return render_template('404.html'), HTTPStatus.NOT_FOUND
    return redirect(url_map.original)
