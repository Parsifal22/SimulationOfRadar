import uuid
import time
import math
from utils import quadratic_bezier

class FlyingObject:
    def __init__(self, canvas, x, y, speed, payload):
        self.object_id = str(uuid.uuid4())
        self.x = x
        self.y = y
        self.angle = None
        self.speed = speed
        self.expire_time = time.time()
        self.payload = bytes.fromhex(payload)
        self.canvas = canvas

    def _set_angle(self, dest_x, dest_y):
        # Calculate angle based on direction vector towards the destination
        dx = dest_x - self.x
        dy = dest_y - self.y

        # Calculate the angle in radians
        self.angle = math.atan2(dy, dx)

    def move(self, dest_x, dest_y, way_x, way_y, bezier_curve):

        # Calculate the distance between the current position and the destination
        distance_to_destination = math.sqrt((self.x - dest_x) ** 2 + (self.y - dest_y) ** 2)
        print(distance_to_destination)
        # Calculate the time it would take to cover the distance in real time
        real_time_duration = distance_to_destination / (self.speed / 1000)  # Convert speed to km/s
        print(real_time_duration/3600)
        # Determine the number of steps needed to cover the distance in real time
        steps = int(real_time_duration / 0.02)  # Assuming a step size of 0.02 seconds
        print(steps)
        # Calculate the step size based on the number of steps
        t_step = 1 / steps
        print("steps: ", t_step)
        t = 0
        for _ in range(steps):
            # Calculate Bezier curve coordinates
            x, y = quadratic_bezier(t, (bezier_curve[0], bezier_curve[1]),
                                    (bezier_curve[2], bezier_curve[3]),
                                    (bezier_curve[4], bezier_curve[5]))

            # Move the object on the canvas
            self.canvas.coords(self.object_id, x - 5, y - 5, x + 5, y + 5)

            # Increment parameter t for the next point on the curve
            t += t_step

            # Update the angle, expire time, and sector every 150 ms
            if time.time() > self.expire_time:
                self._set_angle(dest_x, dest_y)
                self.expire_time = time.time() + 0.15  # expire time updated
                # Update the sector information (you may need to implement this part)

            # Sleep for a short duration to control the rate of object movement
            time.sleep(0.02)