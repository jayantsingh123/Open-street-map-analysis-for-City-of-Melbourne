from pymongo import MongoClient
import json
client=MongoClient()
db=client.test

nodes=db.sample.find({"type":"node"})

node_count=db.sample.count({"type":"node"})#gives the ocunt of nodes, single points


way_count=db.sample.count({"type":"way"})

#created_by is  a field used to describe the computer program which made the
# changes. first count number of documents that contain field .
#next, we count the distinct values of field 'created_by'

created_by_count=db.sample.find({"created_by":{"$exists":1}}).count()


#gives the number of distinct values for field, created_by.
distinct_values=db.sample.distinct("created_by")


#first get the docs with user as melb_guy

docs_melb_guy=db.sample.find({"created.user": "melb_guy"})



#get the count of docs for each user using group by option

group_user=db.sample.aggregate([{
        "$group" : {
           "_id" :"$created.user" ,
           "count": { "$sum":1}}},{"$sort":{"count":-1}}])

list_new=[doc for doc in group_user]# gives the list of dictionaries with
#having the user id and coresponding document ocunt for that user

#Similarly we can find most frequent amenities

#using aggregation pipeline,first need to know where the amenity field exists
#using match operator, followed by 'group' option to find the number of
#occurences per amenity. We sort it in descending order to find the most
#common amenity.


group_amenity=db.sample.aggregate([{"$match":{"amenity":{"$exists":1}}},{
        "$group" : {
           "_id" :"$amenity" ,
           "count": { "$sum":1}}},{"$sort":{"count":-1}}])


 
