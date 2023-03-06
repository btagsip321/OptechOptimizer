import os
import json
from buildpc import *
from flask import Flask, jsonify, request, render_template

Brands = {
    "amd": "AMD",
    "nvidia": "Nvidia",
    "intel": "Intel",
    "nopref": None
}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/build', methods=['GET'])
def build():
    budget = buildBudget(int(request.args.get('budget')), request.args.get('windows')=="on")
    pc_build = buildPc(budget, Brands[request.args.get('cpu')], Brands[request.args.get('gpu')])
    return render_template('results.html', **pc_build)

@app.route('/budget', methods=['GET'])
def budget():
    info = json.loads(request.data)
    return jsonify(buildBudget(info.budget, info.windows))

if __name__ == '__main__':
    print("Running web server")
    port = int(os.environ.get('PORT', 5000))
    print("Port: ", port)
    app.run(host='0.0.0.0', port=port, debug=True)