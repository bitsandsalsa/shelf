import os.path

from flask import Flask


app = Flask(__name__)
app.config.from_pyfile(os.path.join(app.root_path, 'config.py'))

import shelf.view
