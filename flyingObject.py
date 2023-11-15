import re
import string
import random
import os
import time
import math
import json
import threading
from utils import quadratic_bezier, determine_sector

class FlyingObject:
    def __init__(self, canvas, x, y, speed, time_frame):

        self.object_id = self._generate_matching_string()

        # Lock for file access synchronization
        self.file_access_lock = threading.Lock()
        self.x = x
        self.y = y
        self.angle = None
        self.speed = speed

        self.time_frame = time_frame
        self.created_time = time_frame.get_current_time()
        self.expire_time = time.time()
        self.payload = self._generate_random_hex_payload(100)
        self.canvas = canvas


    def _set_angle(self, dest_x, dest_y):
        # Calculate angle based on direction vector towards the destination
        dx = dest_x - self.x
        dy = dest_y - self.y

        # Calculate the angle in radians
        self.angle = math.atan2(dy, dx)

    def _generate_random_hex_payload(self, size):
        random_bytes = os.urandom(size)
        return random_bytes.hex()

    def _generate_matching_string(self):
        characters = string.ascii_lowercase + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(32))
        return random_string

    def _validate_matching_string(self):
        pattern = re.compile(r'[0-9a-z]{32}', re.MULTILINE | re.UNICODE)
        return bool(pattern.match(self.object_id))
    def _serialize_data(self):
        data = {
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "angle": round(self.angle, 2) if self.angle is not None else None,
            "current_time": self.time_frame.get_current_time().strftime("%Y-%m-%dT%H:%M:%S"),
            "sector": determine_sector(self.x, self.y)
        }
        return data

    def _write_to_json(self, data, counter_json, bezier_curve):
        # Acquire the lock before performing file access
        with self.file_access_lock:
            try:
                with open("data.json", "r") as file:
                    file_contents = file.read()
                    existing_data = json.loads(file_contents) if file_contents else {}
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error reading existing data file: {e}")
                existing_data = {}

            if "Flying_Object" + str(counter_json) not in existing_data:
                existing_data["Flying_Object" + str(counter_json)] \
                    = {"object_id": self.object_id,
                       "initial_time": self.created_time.strftime("%Y-%m-%dT%H:%M:%S"),
                       "end_time": self.time_frame.get_current_time().strftime("%Y-%m-%dT%H:%M:%S"),
                       "payload": self.payload,  # Convert bytes to string for JSON serialization
                       "expire_time": self.expire_time,
                       "speed_(m/s)": self.speed,
                       "data": []}

            existing_data["Flying_Object" + str(counter_json)]["data"].extend(data)

            with open("data.json", "w") as file:
                json.dump(existing_data, file, indent=2)


    def _set_expire_time(self, dest_x, dest_y):
        # Calculate the distance between the current position and the destination
        distance_to_destination = math.sqrt((self.x - dest_x) ** 2 + (self.y - dest_y) ** 2)

        # Calculate the time it would take to cover the distance in real time
        real_time_duration = distance_to_destination / (self.speed / 1000)  # Convert speed to km/s

        self.expire_time = real_time_duration / 3600  # expire time in minutes

    def move(self, dest_x, dest_y, bezier_curve, counter_json):

        # Calculate the distance between the current position and the destination
        distance_to_destination = math.sqrt((self.x - dest_x) ** 2 + (self.y - dest_y) ** 2)

        # Calculate the time it would take to cover the distance at the specified speed
        real_time_duration = distance_to_destination / (self.speed / 1000)  # Convert speed to km/s

        self.expire_time = real_time_duration / 60  # Expire time in minutes

        # Determine the number of steps needed to cover the distance in real time
        steps = int((real_time_duration / 60) / 0.15)  # Assuming a step size of 0.02 seconds
        # # Calculate the step size based on the number of steps
        t_step = 1 / steps
        t = 0
        data = []
        for _ in range(steps):
            # Calculate Bezier curve coordinates
            self.x, self.y = quadratic_bezier(t, (bezier_curve[0], bezier_curve[1]),
                                    (bezier_curve[2], bezier_curve[3]),
                                    (bezier_curve[4], bezier_curve[5]))

            # Move the object on the canvas
            self.canvas.coords(self.object_id, self.x - 5, self.y - 5, self.x + 5, self.y + 5)

            # Increment parameter t for the next point on the curve
            t += t_step



            self._set_angle(dest_x, dest_y)
            # Serialize the data and write it to the data.json file
            data.append(self._serialize_data())

            # Sleep for a short duration to control the rate of object movement
            time.sleep(0.15)

        self._write_to_json(data, counter_json, bezier_curve)
