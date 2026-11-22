from flask import flash, redirect, render_template, request

from yacut import app
from yacut.disk import upload_files_to_disk
from yacut.error_handlers import ShortIdGenerationError
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        try:
            url_map = URLMap.create(
                original=form.original_link.data,
                custom_id=form.custom_id.data
            )
        except (ValueError, ShortIdGenerationError) as error:
            flash(str(error))
            return render_template('index.html', form=form)

        return render_template(
            'index.html',
            form=form,
            short_link=url_map.get_absolute_url()
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
            try:
                url_map = URLMap.create(original=original_url)
                results.append(
                    {
                        'filename': filename,
                        'short_link': url_map.get_absolute_url()
                    }
                )
            except (ValueError, ShortIdGenerationError) as error:
                flash(f'Ошибка при обработке файла {filename}: {error}')

        return render_template('files.html', form=form, results=results)

    return render_template('files.html', form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
