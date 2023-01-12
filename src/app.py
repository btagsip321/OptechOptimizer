import os
import json
from buildpc import *
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Sample web app'

@app.route('/build', methods=['GET'])
def build():
    info = json.loads(request.data)
    jsonify(buildBudget(info.budget, info.windows))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)