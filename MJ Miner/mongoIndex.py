import json
import pymongo
from collections import Counter
from pymongo import MongoClient

client = MongoClient()
db = client[ "MidJourney" ] # makes a test database called "testdb"
col = db[ "Prompts" ] #makes a collection called "testcol" in the "testdb"

#Create a custom index for the row "full_command" in the type text
col.create_index([("full_command", pymongo.TEXT)])

#Create a custom index for the row "sortBy" in ascending order
col.create_index([("SortBy", pymongo.ASCENDING)])

#Create a custom index for the row "enqueue_time" in descending order
col.create_index([("enqueue_time", pymongo.DESCENDING)])

#Create a custom index for the row "ranking_score_average" in descending order
col.create_index([("ranking_score_average", pymongo.DESCENDING)])

#Create a compound index for the row "user_ranking_count" in descending order and "ranking_score_average"  in descending order
col.create_index([("user_ranking_count", pymongo.DESCENDING), ("ranking_score_average", pymongo.DESCENDING)])

#Create a compound index for the row "user_ranking_