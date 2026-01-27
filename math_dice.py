import random

#Setup of the Dice
rolls=30
diceSides=12

#Core Functions
def diceRoll():
    allRolls = []
    for _ in range(rolls):
        results = random.randint(1,diceSides)
        allRolls.append(results)
    return allRolls

def sort_list(allRolls):
    sortedList = sorted(allRolls)
    return sortedList

#Probabilities
def getStats(allRolls, diceSides):
    total = {}
    for rollResult in range(1,diceSides+1):
        total[rollResult] = allRolls.count(rollResult)
    return total

def showChart(allRolls, sortedList, total):
    cleanList = " - ".join(str(n) for n in allRolls)
    print(f"{rolls} mal mit eienm {diceSides}-seitigen Würfel gewürfelt.\nHier die unsortierte Urliste: {cleanList}")
    cleanSorted = " - ".join(str(n) for n in sortedList)
    print(f"Und hier die sortierte Liste: {cleanSorted}") 
    maxCount = max(total.values())
    scale = 25
    labelWidth = len(str(diceSides))
    for face, count in total.items():
        rel = count / rolls
        barLength = int(count / maxCount * scale)
        bar = "█" * barLength
        print(f"{face:<{labelWidth}}: |{bar:<{scale}}| ({count}) -> {rel:.1%}")

if __name__ == "__main__":
    if rolls>0:
        allRolls = diceRoll()
        sortedList = sort_list(allRolls)
        total = getStats(allRolls, diceSides)
        showChart(allRolls, sortedList, total)