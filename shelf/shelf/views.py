import os.path
import random
import string

from flask import g, render_template, flash, redirect, url_for, request, abort, send_file
from flask.ext import uploads

from shelf import app
from shelf.database import get_db, query_db

documents = uploads.UploadSet('documents', uploads.DOCUMENTS + uploads.TEXT + ('pdf', 'ppt'))
uploads.configure_uploads(app, documents)


@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

class Document(object):
    doc_id_chars = string.letters + string.digits

    def __init__(self, fs_name, friendly_name):
        self.fs_name = fs_name
        self.friendly_name = friendly_name
        self.doc_id = None

    @classmethod
    def gen_doc_id(cls):
        return ''.join(random.sample(cls.doc_id_chars, 5))

    def store(self):
        self.doc_id = self.gen_doc_id()
        g.db.execute(
            'insert into documents (document_id, fs_name, friendly_name) values (?, ?, ?)',
            [self.doc_id, self.fs_name, self.friendly_name]
        )
        g.db.commit()

    @classmethod
    def load(cls, doc_id):
        filename_res = query_db('select fs_name, friendly_name from documents where document_id=''?''', [doc_id], True)
        if filename_res:
            return Document(filename_res['fs_name'], filename_res['friendly_name'])
        else:
            return None

## routes ##

@app.route('/')
def show_entries():
    entries = query_db(' '.join([
        'SELECT statuses.status, formats.format, entries.citation, entries.document_id, entries.summary, documents.friendly_name',
        'FROM entries',
        'INNER JOIN statuses ON statuses.id=entries.status_id',
        'INNER JOIN formats ON formats.id=entries.format_id',
        'INNER JOIN documents ON documents.document_id=entries.document_id'
    ]))
    return render_template(
        'show_entries.html',
        entries=entries,
        docs_dir=documents.config.destination
    )

@app.route('/add', methods=['POST'])
def add_entry():
    friendly_name = request.files['document'].filename
    if '..' in friendly_name or '/' in friendly_name:
        flash('Bad filename')
        return redirect(url_for('show_entries'))

    fs_name = documents.save(request.files['document'])
    doc = Document(fs_name, friendly_name)
    doc.store()

    g.db.execute(
        'insert into entries (status_id, format_id, citation, document_id, summary) values (?, ?, ?, ?, ?)',
        [
            request.form['status'],
            request.form['format'],
            request.form['citation'],
            doc.doc_id,
            request.form['summary']
        ]
    )
    g.db.commit()

    flash('New entry was successfully added')
    return redirect(url_for('show_entries'))

@app.route(app.config['UPLOADED_DOCUMENTS_URL'] + '<doc_id>')
def show_doc(doc_id):
    doc = Document.load(doc_id)
    if doc is None:
        abort(404)
    return send_file(
        documents.path(doc.fs_name),
        **{'as_attachment': True, 'attachment_filename': doc.friendly_name}
    )
