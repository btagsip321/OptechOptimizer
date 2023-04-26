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

    # Variables
    budgetTotal = int(request.args.get('budget') or 1000) # initial budget input
    tax = float(request.args.get('tax') or 0) # initial tax input

    # Initial budget
    budget = buildBudget(
        budgetTotal, 
        request.args.get('windows')=="on",
        tax
    )

    # Initial PC build
    pc, buildPrice = buildPc(
        budget, 
        Brands[request.args.get('cpu')], 
        int(request.args.get('ssdStorage') or 256), 
        int(request.args.get('hddStorage') or 1000),
    )

    # Debug initial pc build print
    for part in pc.keys():
        budget[part] = extractPrice(pc[part])
    print(pc, budget, buildPrice)

    # Print the initial allocated budget
    print("Before Allocation:", sum(budget.values()) )

    # Remainding price, taxed budget - pc build price
    remainder = (budgetTotal / ((1) + (tax/100))) - float(buildPrice)

    print("Remainder: ", remainder)
    print(budget, sum(budget.values()) )
    
    if request.args.get('allocpref') == "cpu":
        budget["CPU"] = cleanBudget(budget["CPU"] + (remainder), 0, 50000)
    else:
        budget["GPU"] = cleanBudget(budget["GPU"] + (remainder*0.7), 0, 50000)

    print(budget, sum(budget.values()) )

    print("After Allocation:", sum(budget.values()) )

    pc_build, price = buildPc(
        budget, 
        Brands[request.args.get('cpu')], 
        int(request.args.get('ssdStorage') or 256), 
        int(request.args.get('hddStorage') or 1000),
    )

    for part in list(pc_build.keys()):
        if pc_build[part].find("Buy here: "):
            index = pc_build[part].find("Buy here: ")
            pc_build[part + "_URL"] = pc_build[part][index + 10:]
            pc_build[part] = pc_build[part][:index]

    print(pc_build)

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