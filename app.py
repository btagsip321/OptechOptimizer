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
    budget = buildBudget(
        int(request.args.get('budget') or 1000), 
        request.args.get('windows')=="on",
        float(request.args.get('tax') or 0)
    )

    pc, price = buildPc(
        budget, 
        Brands[request.args.get('cpu')], 
        int(request.args.get('ssdStorage') or 256), 
        int(request.args.get('hddStorage') or 1000),
    )

    print(pc, price)
    print("Before Allocation:", sum(budget.values()) )

    remainder = round((float(request.args.get('budget') or 1000)) - float(price))

    print("Remainder: ", remainder)
    
    budget["GPU"] = cleanBudget(extractPrice(pc["GPU"]) + remainder*0.7, 0, 50000)
    budget["CPU"] = cleanBudget(extractPrice(pc["CPU"]) + remainder*0.3, 0, 50000)

    print("After Allocation:", sum(budget.values()) )

    pc_build, price = buildPc(
        budget, 
        Brands[request.args.get('cpu')], 
        int(request.args.get('ssdStorage') or 256), 
        int(request.args.get('hddStorage') or 1000),
    )

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