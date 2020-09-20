import json
import os
from flask import Flask, request, session,jsonify
from werkzeug.utils import secure_filename
import logging
import flask_cors
import sys
sys.path.append('..')

import run_optimization


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')



UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files['file'] 
    filename = secure_filename("HackRiceDataExcel.xlsx")
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    response = jsonify(run_optimization.run())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

flask_cors.CORS(app, expose_headers='Authorization')