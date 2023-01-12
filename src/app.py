import os
from flask import Flask
from buildpc import *

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Sample web app'

#@app.route('/build')(buildBudget)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)