import os
import json
from buildpc import *
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    print('rendering')
    return render_template('index.html')

@app.route('/build', methods=['GET'])
def build():
    budget = buildBudget(int(request.args.get('budget')), False)
    print(budget)
    pc_build = buildPc(budget)
    print(pc_build)
    return jsonify(pc_build)

@app.route('/budget', methods=['GET'])
def budget():
    info = json.loads(request.data)
    jsonify(buildBudget(info.budget, info.windows))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)