from pymongo import MongoClient
import pymongo

client = MongoClient()
db = client[ "MidJourney" ] # makes a test database called "testdb"
col = db[ "Prompts" ] #makes a collection called "testcol" in the "testdb"

print(col.aggregate([{"$group": {"_id": "$full_command"}}, {"$group": {"_id": 1, "count": {"$sum": 1}}}]))