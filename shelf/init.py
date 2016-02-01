#NOTE: Be sure to delete database file and uploads directory before running this

import shutil
import os

from shelf import app
from shelf.model import init_db


# we should be using SQLALCHEMY_DATABASE_URI, but we would have to parse URI
db_file = os.path.join('shelf', 'shelf.db')
upload_dir = app.config['UPLOADED_DOCUMENTS_DEST']

print 'This will delete database file "{}" and upload directory "{}".'.format(db_file, upload_dir)
res = raw_input('Continue? [y|n]')
if res == 'y':
    try:
        shutil.rmtree(upload_dir)
        os.unlink(db_file)
    except OSError:
        pass

    init_db()
