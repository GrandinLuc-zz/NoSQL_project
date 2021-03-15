from pymongo import MongoClient
from random import randint
import json

#Step 1: Connect to MongoDB - Note: Change connection string as needed
myclient = MongoClient(port=27017)
mydbNOSQL=myclient['local']
mycol = mydbNOSQL["dossier"]
print(mydbNOSQL.list_collection_names())

#multiple insertion
x = mycol.insert_many(info_total_dict())
print(x.inserted_ids)

for x in mycol.find():
    print(x)

mycol.drop()