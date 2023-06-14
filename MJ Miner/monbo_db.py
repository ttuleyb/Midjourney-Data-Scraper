#Read a json file and add it to mongodb
import json
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client[ "MidJourney" ] # makes a test database called "testdb"
col = db[ "Prompts" ] #makes a collection called "testcol" in the "testdb"
    
from fileinput import filename
from json import load
import os
from pathlib import Path
from multiprocessing.pool import ThreadPool
from collections import Counter
import time
import random
import math
import logging

paths = Path("jsons").glob("**/*.json") #Script for reading all subdirectories Path("jsons").glob("**/*.json") *.json for only this dir

everything = []

jobsToDo = len(list(Path("jsons").glob("**/*.json")))
jobsDone = 0

prefix_dict = {'m_':'voting', 'r_':'rising', 'h_':'hot', 'n_':'new', 'tw_':'top-week', 'tt_':'top-today', 'tm_':'top-month', 'ta_':'top-all'}

def add_to_mongoDB(file):
    global jobsDone
    filePath = file.resolve()
    try:
        if os.path.getsize(filePath) < 10000:
            os.remove(filePath)
            return
        with open(filePath, encoding="utf-8") as f:
            # col.insert_many(json.loads(f.read()))
            global everything

            fileNameWithoutExt = os.path.basename(file).split(".")[0]
            num = ""

            if not "_" in fileNameWithoutExt:
                sort = "Top-All"
                num = fileNameWithoutExt
            else:
                num = fileNameWithoutExt.split("_")[1]
                fileSortPref = fileNameWithoutExt.split("_")[0] + "_"
                sort = prefix_dict.get(fileSortPref)

            data = json.loads(f.read())
            for i in range(len(data)):
                data[i]["sortBy"] = sort
                data[i]["PageNum"] = int(num)
            col.insert_many(data)

    except Exception as e:
        logging.error('Error at %s', 'division', exc_info=e)

    print(str((jobsDone/jobsToDo)*100) + "  " + str(file.name))
    jobsDone += 1

with ThreadPool(12) as p:
    p.map(add_to_mongoDB, paths)

# for i in paths:
#     add_to_mongoDB(i)
