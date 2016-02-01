import os.path
import random
import string

from flask import render_template, flash, redirect, url_for, request, abort, send_file
from flask.ext import uploads

import model
from model import db
from shelf import app


documents = uploads.UploadSet('documents', uploads.DOCUMENTS + uploads.TEXT + ('pdf', 'ppt'))
uploads.configure_uploads(app, documents)


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
        db.session.add(model.Document(self.doc_id, self.fs_name, self.friendly_name))
        db.session.commit()

    @classmethod
    def load(cls, doc_id):
        filename_res = model.Document.query.filter_by(document_id=doc_id).first()
        if filename_res:
            return Document(filename_res.fs_name, filename_res.friendly_name)
        else:
            return None

## routes ##

@app.route('/')
def show_entries():
    entries = model.Entry.query.all()
    return render_template(
        'show_entries.html',
        entries=entries,
        docs_url=documents.config.base_url,
        allowed_exts=documents.extensions
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

    db.session.add(model.Entry(
        request.form['status'],
        request.form['format'],
        request.form['citation'],
        doc.doc_id,
        request.form['summary']
    ))
    db.session.commit()

    flash('New entry was successfully added')
    return redirect(url_for('show_entries'))

@app.route(app.config['UPLOADED_DOCUMENTS_URL'] + '<doc_id>')
def show_doc(doc_id):
    doc = Document.load(doc_id)
    if doc is None:
        abort(404)
    return send_file(
        os.path.join('..', documents.path(doc.fs_name)),
        **{'as_attachment': True, 'attachment_filename': doc.friendly_name}
    )
