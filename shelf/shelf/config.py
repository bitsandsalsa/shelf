import os.path


DEBUG = True
SECRET_KEY='S\x9eEQ@Hd\x08\x00\x87=\x12{@"\xcfk\xd8\xb9\xb0\xff\xae\xe0\x85'

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///shelf.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Uploads
UPLOADED_DOCUMENTS_DEST = os.path.join('shelf', 'documents')
UPLOADED_DOCUMENTS_URL = '/documents/'
