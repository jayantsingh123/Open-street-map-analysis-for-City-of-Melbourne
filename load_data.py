
#Here, we load the json file into database, test in mongodb.

from pymongo import MongoClient
import json
client=MongoClient()
db=client.test  #make a database called test

with open('sample_file_osm.json') as f_in:
    #each line is  a JSON array, so we need to loop through
    for item in f_in:
        data = json.loads(item)
        #sample is  a collection in test databse
        db.sample.insert(data) 
