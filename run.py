#! /usr/bin/python
import os
from app import app

UPLOAD_FOLDER = '.'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5060))
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(host='0.0.0.0', port=port, debug = True)
