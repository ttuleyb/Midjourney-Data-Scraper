from fileinput import filename
from json import load
import os
from pathlib import Path
from multiprocessing.pool import ThreadPool
from collections import Counter
import time
import random
import math

paths = Path("jsons").glob("**/*.json") #Script for reading all subdirectories Path("jsons").glob("**/*.json") *.json for only this dir

everything = []

jobsToDo = len(list(Path("jsons").glob("**/*.json")))
jobsDone = 0

def read_to_memory(file):
    global jobsDone
    filePath = file.resolve()
    try:
        if os.path.getsize(filePath) < 10000:
            os.remove(filePath)
            return
        with open(filePath, "r", encoding="utf-8") as inputFile:
            global everything
            data = load(inputFile)
            if random.randint(0, 60) == 15:
                print(str((jobsDone/jobsToDo)*100) + "  " + str(file.name))
            for i in data:
                everything.append(i["full_command"])
    except:
        print("Error")

    jobsDone += 1

with ThreadPool(12) as p:
    p.map(read_to_memory, paths)

print("Everything:")

duplicates = 0

with open("everything.txt", "w", encoding="utf-8") as f:
        f.write("")

everythingStr = ""

# for i in range(math.floor(len(everything) / 1000000)):
#     with open("everything.txt", "a", encoding="utf-8") as f:
#         f.write("\n".join(everything[(i-1) * 1000000 : i * 1000000]))
#         f.write("\n")
#     with open(f"everything_{i}.txt", "a", encoding="utf-8") as f:
#         f.write("\n".join(everything[(i-1) * 1000000 : i * 1000000]))
#         f.write("\n")

with open("everything.txt", "a", encoding="utf-8") as f:
    f.write("\n".join(everything))
    f.write("\n")

# everythingStr = "\n".join(everything)

# for i in everything:
#     with open("everything.txt", "a", encoding="utf-8") as f:
#         f.write(i + "\n")

counter_object = Counter(everything)
keys = counter_object.keys()
num_values = len(keys)
print(str(num_values) + " unique items found!")
print(str(len(everything)) + " total number of items found")

#import data_counter