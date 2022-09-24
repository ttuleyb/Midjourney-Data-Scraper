import os
from pathlib import Path

paths = Path("jsons").glob("**/*.json")

names = []

for i in paths:
    names.append([str(os.path.basename(i)).split(".")[0], str(i).split("_")[0]])
    
prefixes = ["r", "h", "n", "tw", "tt", "ta", "tm", ""]
highestNums = {}

for prefix in prefixes:
    highestNum = 0

    for i in names:
        if i[0].split("_")[0] == prefix:
            if highestNum < int(i[0].split("_")[1]):
                highestNum = int(i[0].split("_")[1])
    highestNums[prefix] = highestNum

specialNames = []

for prefix in prefixes:
    specialty = 0
    
    for i in names:
        if specialty == 5:
            break
        if i[0].split("_")[0] == prefix:
            if int(i[0].split("_")[1]) >= dict.get(highestNums, prefix) - 50:
                specialNames.append(i[0])
                specialty += 1

print(specialNames)