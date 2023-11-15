from flask import Flask, request, jsonify
import json
from datetime import datetime
import math

app = Flask(__name__)

def calculate_trajectory(entry, speed):
    # Check if speed is not None
    if speed is None:
        return {"x": None, "y": None}

    # Calculate trajectory based on speed, angle, and time
    # Extract minutes and convert to seconds
    time_minutes = float(entry.get("current_time").split(":")[1])  # Extract minutes and convert to float
    time = time_minutes * 60  # Convert minutes to seconds
    angle = entry.get("angle")
    x = entry.get("x")
    y = entry.get("y")

    # Check if time, angle, x, and y are not None
    if time is None or angle is None or x is None or y is None:
        return {"x": None, "y": None}

    trajectory_x = x + speed * time * math.cos(math.radians(angle))
    trajectory_y = y + speed * time * math.sin(math.radians(angle))

    return {"x": trajectory_x, "y": trajectory_y}


@app.route('/')
def hello():
    return "It is the main page"


@app.route('/query1', methods=['GET'])
def query1():
    # Query #1 – pull a specific object trajectory from an arbitrary beginning of time to the end of a time interval
    object_id = request.args.get('object_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Validate input parameters
    if not object_id or not start_time or not end_time:
        return jsonify({"error": "Invalid parameters. Please provide object_id, start_time, and end_time."}), 400

    try:
        # Check if start_time and end_time are in the correct format
        datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({"error": "Invalid datetime format. Please use the format %Y-%m-%dT%H:%M:%S."}), 400

    # Read data from the JSON file
    with open('data.json') as f:
        log_data = json.load(f)

    # Get the trajectory data for the specified object
    object_data = log_data.get(object_id, {})
    trajectory_data = object_data.get('data', [])

    # Filter trajectory data based on the specified time interval
    start_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
    end_datetime = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')

    result = [
        {
            "payload": object_data.get('payload'),
            "speed": object_data.get('speed_(m/s)'),
            "angle": entry.get("angle"),
            "x": entry.get("x"),
            "y": entry.get("y"),
            "current_time": entry.get("current_time"),
            "trajectory": calculate_trajectory(entry, object_data.get('speed_(m/s)'))
        }
        for entry in trajectory_data
        if start_datetime <= datetime.strptime(entry['current_time'], '%Y-%m-%dT%H:%M:%S') <= end_datetime
    ]

    return jsonify(result)


@app.route('/query2', methods=['GET'])
def query2():
    # Query #2 – pull a snapshot from any sector in a given timeframe
    sector_id = request.args.get('sector_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Read data from the JSON file
    with open('data.json') as f:
        log_data = json.load(f)

    result = []

    for object_id, obj_data in log_data.items():
        # Check if the object has data within the specified time range
        relevant_data = [
            entry for entry in obj_data['data']
            if start_time <= entry['current_time'] <= end_time and entry.get('sector') == sector_id
        ]

        if relevant_data:
            # Sort the relevant data by the first appearance inside the queried sector
            relevant_data = sorted(relevant_data, key=lambda x: x['current_time'])

            # Extract the first appearance data
            first_appearance_data = relevant_data[0]

            # Construct the snapshot
            snapshot = {
                "object_id": object_id,
                "speed": obj_data.get('speed_(m/s)'),
                "first_appearance_time": first_appearance_data['current_time'],
                "location": {
                    "x": first_appearance_data['x'],
                    "y": first_appearance_data['y'],
                    "angle": first_appearance_data.get('angle', None)  # Include angle if available
                }
            }

            result.append(snapshot)

    # Sort the result by the first appearance time
    result = sorted(result, key=lambda x: x['first_appearance_time'])

    return jsonify(result)


def run_flask_app():
    app.run()

