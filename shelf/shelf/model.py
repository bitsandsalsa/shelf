from flask_sqlalchemy import SQLAlchemy

from shelf import app


db = SQLAlchemy(app)

def init_db():
    """Initializes the database."""
    db.create_all()

    db.session.add_all([
        Status('done'),
        Status('pending'),
        Status('unread'),
        Format('conference paper'),
        Format('conference presentation'),
        Format('vendor whitepaper'),
    ])

    db.session.commit()

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text, nullable=False)

    def __init__(self, status):
        self.status = status

    def __repr__(self):
        return '<Status "{}">'.format(self.status)

class Format(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    format = db.Column(db.Text, nullable=False)

    def __init__(self, format):
        self.format = format

    def __repr__(self):
        return '<Format "{}">'.format(self.format)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Text, nullable=False, unique=True)
    fs_name = db.Column(db.Text, nullable=False)
    friendly_name = db.Column(db.Text)

    def __init__(self, document_id, fs_name, friendly_name):
        self.document_id = document_id
        self.fs_name = fs_name
        self.friendly_name = friendly_name

    def __repr__(self):
        return '<Document (document_id="{}", fs_name="{}", friendly_name="{}")>'.format(
            self.document_id,
            self.fs_name,
            self.friendly_name
        )

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status')
    format_id = db.Column(db.Integer, db.ForeignKey('format.id'))
    format = db.relationship('Format')
    citation = db.Column(db.Text, nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.document_id'))
    document = db.relationship('Document')
    summary = db.Column(db.Text)

    def __init__(self, status_id, format_id, citation, document_id, summary):
        self.status_id = status_id
        self.format_id = format_id
        self.citation = citation
        self.document_id = document_id
        self.summary = summary
