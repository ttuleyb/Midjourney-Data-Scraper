#Read a json file and add it to mongodb
import json
import pymongo
from pymongo import MongoClient
from fileinput import filename
import os
from pathlib import Path
from multiprocessing.pool import ThreadPool
from collections import Counter
import time
import random
import math

paths = Path("jsons").glob("**/*.json") #Script for reading all subdirectories Path("jsons").glob("**/*.json") *.json for only this dir

client = MongoClient()
db = client[ "MidJourney" ] # makes a test database called "testdb"
col = db[ "Prompts" ] #makes a collection called "testcol" in the "testdb"

#rising, hot, new, top-week, top-today, top-month, top-all
#top-all is default
#otherwise, r_, h_, n_, tw_, tt_, tm_, ta_

prefix_dict = {'r_':'rising', 'h_':'hot', 'n_':'new', 'tw_':'top-week', 'tt_':'top-today', 'tm_':'top-month', 'ta_':'top-all'}

for i in range(10000):
    file = next(paths)

with open(file.resolve(), encoding="utf-8") as f:
    # col.insert_many(json.loads(f.read()))
    global everything

    fileNameWithoutExt = os.path.basename(file).split(".")[0]

    if not "_" in fileNameWithoutExt:
        sort = "Top-All"
    else:
        fileSortPref = fileNameWithoutExt.split("_")[0] + "_"
        sort = prefix_dict.get(fileSortPref)

    data = json.loads(f.read())
    for i in range(len(data)):
        data[i]["sortBy"] = sort
    col.insert_many(data)