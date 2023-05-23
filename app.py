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
        int(request.args.get('ssdStorage') or 0), 
        int(request.args.get('hddStorage') or 0),
        int(request.args.get('ramStorage') or 0),
        False
    )

    # Debug initial pc build print
    for part in pc.keys():
        budget[part] = extractPrice(pc[part])

    # Print the initial allocated budget
    print("Before Allocation:", sum(budget.values()) )

    # Remainding price, taxed budget - pc build price
    remainder = (budgetTotal / ((1) + (tax/100))) - float(buildPrice)

    # Reallocation
    for part in parts:
        # Leave $25 for other reallocation
        if remainder <= 25: 
            print("Stopping at", part) 
            break
        
        # Add remainder to budget in part
        budget[part] = cleanBudget(budget[part] + remainder, 0, 50000)

        # Calculate new PC
        pc_build, price = buildPc(
            budget, 
            Brands[request.args.get('cpu')], 
            int(request.args.get('ssdStorage') or 0), 
            int(request.args.get('hddStorage') or 0),
            int(request.args.get('ramStorage') or 0),
            request.args.get('windows')=="on",
        )

        # Set the new prices
        for x in pc_build.keys():
            budget[x] = extractPrice(pc_build[x])

        # Calculate new remainder
        remainder = (budgetTotal / ((1) + (tax/100))) - float(price)
        print("reallocating", part, "remainder:", remainder, "price:", price) 

    def reallocate(part, amt, max, remainder):
        if remainder <= 0: return remainder
        pc_build[part] = "$" + str(cleanBudget(extractPrice(pc_build[part]) + remainder*amt, 0, max)) + " (Input budget into PC Part Picker)"
        price = sum(map(extractPrice, pc_build.values())) + (140 if (request.args.get('windows')=="on") else 0)
        return budgetTotal - price


    # Reallocate remainder into non url components
    remainder = reallocate("Motherboard", .5, 700, remainder)
    remainder = reallocate("PSU", .5, 1000, remainder)
    remainder = reallocate("CPU_Cooler", 1, 305, remainder)
    remainder = reallocate("Motherboard", 1, 700, remainder)
    remainder = reallocate("PSU", 1, 1000, remainder)
    remainder = reallocate("CPU_Cooler", 1, 305, remainder)
    print(remainder)

    price = sum(map(extractPrice, pc_build.values())) + (140 if (request.args.get('windows')=="on") else 0)
    remainder = budgetTotal - price

    # Calculate new total price
    price = sum(map(extractPrice, pc_build.values())) + (140 if (request.args.get('windows')=="on") else 0)
    pc_build["Total_Price"] = "$" + format(price, ".3f")

    # Add URLs to build
    for part in list(pc_build.keys()):
        if pc_build[part].find("Buy here: "):
            index = pc_build[part].find("Buy here: ")
            pc_build[part + "_URL"] = pc_build[part][index + 10:]
            pc_build[part] = pc_build[part][:index]

    # Add windows key and URL
    pc_build["Windows_Key"] = "$" + str(140 if (request.args.get('windows')=="on") else 0)
    pc_build["Windows_URL"] = "https://www.amazon.com/Windows-11-Home-Digital-Download/dp/B09WCHGP12/ref=sr_1_3?keywords=windows%2B11%2Bhome&qid=1683027821&sr=8-3&th=1" if (request.args.get('windows')=="on") else "https://support.microsoft.com/en-us/windows/create-installation-media-for-windows-99a58364-8c02-206f-aa6f-40c3b507420d"
    
    # Render results
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
