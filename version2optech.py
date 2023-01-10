budget = int(input("Please enter your budget: "))
gpuPercentage = .4
cpuPercentage = .3
storageDedication = int(input("Please enter your desired HDD storage. Ensure it is an increment of 250"))
ssdDedication = int(input("Please enter your desired SSD storage. Ensure it is an increment of 250"))
storageIncrements = (storageDedication/250) * 25
ssdIncrements = (ssdDedication/250) * 25
if(budget > 1000):
    caseCost = 100
elif(budget > 750):
    caseCost = 70
else:
    caseCost = 40

budget = budget - storageIncrements - ssdIncrements - caseCost

windowsNow = input("Do you want to buy a windows key with your computer? We suggest you buy it later. Write 'Y' for YES and 'N' for NO")
if(windowsNow == 'Y'):
    windowsSource = input("Do you want to buy windows from Microsoft or a third-party? We suggest finding a reputable third-party, key costs can be as low as $10 whereas buying from Microsoft is $100.  Write 'Y' for MICROSOFT and 'N' for THIRD-PARTY")
    if(windowsSource == 'Y'):
        budget = budget - 100
    else:
        budget = budget - 10
gpuBudget = budget * gpuPercentage
cpuBudget = budget * cpuPercentage
budgetUpdated = budget - gpuBudget - cpuBudget
ramBudget = budgetUpdated * .3
psuBudget = budgetUpdated * .3
moboBudget = budgetUpdated * .3
coolerBudget = budgetUpdated * .1
print("GPU: " + str(gpuBudget) + " CPU: " + str(cpuBudget) + " Cooler: " + str(coolerBudget) + " RAM: " + str(ramBudget) + " MOBO: " + str(moboBudget) + " HDD: " + str(storageIncrements) + " SSD: " + str(ssdIncrements) + " Case: " + str(caseCost))
