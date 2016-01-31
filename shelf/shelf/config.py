import os.path


DATABASE = os.path.join('shelf', 'shelf.db')
DEBUG = True
SECRET_KEY='S\x9eEQ@Hd\x08\x00\x87=\x12{@"\xcfk\xd8\xb9\xb0\xff\xae\xe0\x85'

# uploads
UPLOADED_DOCUMENTS_DEST = os.path.join('shelf', 'documents')
UPLOADED_DOCUMENTS_URL = '/documents/'
