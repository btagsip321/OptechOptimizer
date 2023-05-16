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

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html')

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
        False
    )

    # Debug initial pc build print
    for part in pc.keys():
        budget[part] = extractPrice(pc[part])

    # Print the initial allocated budget
    print("Before Allocation:", sum(budget.values()) )

    # Remainding price, taxed budget - pc build price
    remainder = (budgetTotal / ((1) + (tax/100))) - float(buildPrice)

    print(parts)
    for part in parts:
        print(part)
        if remainder <= 25: 
            print("stopping at", part) 
            break
        
        budget[part] = cleanBudget(budget[part] + remainder, 0, 50000)
        pc_build, price = buildPc(
            budget, 
            Brands[request.args.get('cpu')], 
            int(request.args.get('ssdStorage') or 256), 
            int(request.args.get('hddStorage') or 1000),
            request.args.get('windows')=="on",
        )

        for part in pc_build.keys():
            budget[part] = extractPrice(pc_build[part])

        remainder = (budgetTotal / ((1) + (tax/100))) - float(price)
        print("reallocating", part, "remainder:", remainder, "price:", price) 

    print(pc_build)
    print(pc_build["CPU_Cooler"])
    print(remainder*.2)
    pc_build["Motherboard"] = "$" + str(cleanBudget(extractPrice(pc_build["Motherboard"]) + remainder*.5, 0, 700)) + " (Input budget into PC Part Picker)"
    pc_build["PSU"] = "$" + str(cleanBudget(extractPrice(pc_build["PSU"]) + remainder*.3, 0, 1000)) + " (Input budget into PC Part Picker)"
    pc_build["CPU_Cooler"] = "$" + str(cleanBudget(extractPrice(pc_build["CPU_Cooler"]) + remainder*.2, 0, 305)) + " (Input budget into PC Part Picker)"

    #if request.args.get('allocpref') == "cpu":
    #    budget["CPU"] = cleanBudget(budget["CPU"] + (remainder), 0, 50000)
    #elif request.args.get('allocpref') == "gpu":
    #    budget["GPU"] = cleanBudget(budget["GPU"] + (remainder), 0, 50000)

    #print(pc_build)

    price = sum(map(extractPrice, pc_build.values())) 
    print(price)
    

    if(request.args.get('windows')=="on"):
        price = price + 140
    pc_build["Total_Price"] = "$" + format(price, ".3f")

    for part in list(pc_build.keys()):
        if pc_build[part].find("Buy here: "):
            index = pc_build[part].find("Buy here: ")
            pc_build[part + "_URL"] = pc_build[part][index + 10:]
            pc_build[part] = pc_build[part][:index]

    pc_build["Windows_Key"] = "$" + str(140 if (request.args.get('windows')=="on") else 0)
    pc_build["Windows_URL"] = "https://www.amazon.com/Windows-11-Home-Digital-Download/dp/B09WCHGP12/ref=sr_1_3?keywords=windows%2B11%2Bhome&qid=1683027821&sr=8-3&th=1" if (request.args.get('windows')=="on") else "https://support.microsoft.com/en-us/windows/create-installation-media-for-windows-99a58364-8c02-206f-aa6f-40c3b507420d"
    
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
