from flask import Flask, request, jsonify

import sys
import threading
import json

import Database.app_db as app_db

app = Flask(__name__)

lock = threading.Lock()


# Function to create a log. Validates and sends to DB layer.
@app.route('/logs', methods = 'POST')
def create_log():
    if not request.json:
        sys.exit("JSON data not found.")

    events = request.get_json()

    if not events['user_id'].isdigit():
        sys.exit("User ID is not an integer.")

    user_id = events['user_id']
    event_type = events['event_type']
    timestamp = events['timestamp']
    src_service = events['src_service']
    invariant_data = events['invariant_data']
    app_data = events['app_data']

    # Saves the current data so we don't lose information in case the database transaction fails.
    try:
        with lock:
            with open("logs.txt", 'a') as file:
                file.writelines(str(user_id) + str(event_type) + str(timestamp) + str(src_service) + str(invariant_data) + str(app_data))
    except:
        print("Couldn't save logs in text file.")
        
    id, success = app_db.create_log(user_id, event_type, timestamp, src_service, invariant_data, app_data)

    if not success:
        return jsonify({'message' : 'The event could not be added to logs.', 'id':id}), 500

    return jsonify({'message': 'Event added to logs.', 'id' : id}), 201


# Function to fetch all logs.
@app.route('/logs', methods = ['GET'])
def read_logs():
    with open("logs.txt", 'r') as file:
        file.readlines()

    activity = app_db.read_logs()

    page_size = 10
    paged_events = list()
    
    total_pages = len(activity)/page_size
    rem = len(activity) % page_size
    if rem:
        total_pages += 1

    for page_num in range(total_pages):
        start_index = (page_num - 1) * page_size
        end_index = start_index + page_size

        paged_events.append(activity[start_index:end_index])
    
    paged_events = json.loads(paged_events)

    return jsonify({'events': paged_events})


# Function to fetch logs of a particular user.
@app.route('/logs/<user_id>', methods = ['GET'])
def read_logs(user_id):
    if not user_id.isdigit():
        sys.exit("User ID is not an integer.")
    
    activity = app_db.read_logs(str(user_id))

    page_size = 10
    paged_events = list()
    
    total_pages = len(activity)/page_size
    rem = len(activity) % page_size
    if rem:
        total_pages += 1

    for page_num in range(total_pages):
        start_index = (page_num - 1) * page_size
        end_index = start_index + page_size

        paged_events.append(activity[start_index:end_index])
    
    paged_events = json.loads(paged_events)

    return jsonify({'events': paged_events})


# Comment this when using server.
if __name__  ==  '__main__':
    app.run(port = 3000, debug = False, threaded = True)