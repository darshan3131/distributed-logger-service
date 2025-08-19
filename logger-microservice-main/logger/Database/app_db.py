from pymongo import MongoClient

import os

# Using MongoDB for an efficient write-heavy application.
client = MongoClient(
  host = os.getenv('HOST'),
  port = 27017
)

db = client["activity_db"]
collection = db["logger"]

# Sharding the database on user_id to improve throughput.
admin = client.admin
admin.command({'enableSharding':str(db)})
admin.command({'shardCollection': str(collection), 'key': {'user_id' : 1}})


# Function to create logs in database.
def create_log(user_id, event_type, timestamp, src_service, invariant_data, app_data):
    event = {
        'user_id' : user_id,
        'event_type' : event_type,
        'timestamp' : timestamp,
        'src_service': src_service,
        'invariant_data': invariant_data,
        'app_data': app_data
    }
    id = -1
    success = True

    try:
        id = collection.insert_one(event)
    except:
        success = False
    finally:
        return id, success


# Function to read all logs from database.
def read_logs():
    events = []
    
    docs = collection.find({}, {"_id":0}).sort("timestamp").to_json()
    for event in docs:
        events.append(event)
    
    return events


# Function to read logs by user ID.
def read_logs(user_id):
    events = []

    query = {"user_id" : user_id}
    docs = collection.find(query, {"_id":0}).sort("timestamp").to_json()

    for event in docs:
        events.append(event)
    
    return events