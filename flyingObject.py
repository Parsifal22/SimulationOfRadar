import uuid
import time
import math
from utils import quadratic_bezier

class FlyingObject:
    def __init__(self, canvas, x, y, speed, expire_time, payload):
        self.object_id = str(uuid.uuid4())
        self.x = x
        self.y = y
        self.angle = None
        self.speed = speed
        self.expire_time = expire_time
        self.created_time = time.time()
        self.payload = bytes.fromhex(payload)
        self.canvas = canvas

    def _set_angle(self, dest_x, dest_y):
        # Calculate angle based on direction vector towards the destination
        dx = dest_x - self.x
        dy = dest_y - self.y

        # Calculate the angle in radians
        self.angle = math.atan2(dy, dx)

    def move(self, dest_x, dest_y, way_x, way_y, bezier_curve):
        t = 0
        while t <= 1:
            # Calculate Bezier curve coordinates
            x, y = quadratic_bezier(t, (bezier_curve[0], bezier_curve[1]),
                                    (bezier_curve[2], bezier_curve[3]),
                                    (bezier_curve[4], bezier_curve[5]))

            # Move the object on the canvas
            self.canvas.coords(self.object_id, x - 5, y - 5, x + 5, y + 5)

            # Increment parameter t for the next point on the curve
            t += 0.02  # Adjust the step size as needed

            distance_to_waypoint = math.sqrt((self.x - way_x) ** 2 + (self.y - way_y) ** 2)
            distance_to_destination = math.sqrt((self.x - dest_x) ** 2 + (self.y - dest_y) ** 2)

            if distance_to_waypoint <= 5:
                # Object has reached the waypoint, update angle for the next segment
                self._set_angle(dest_x, dest_y)

            if distance_to_destination <= 5:  # Adjust the threshold as needed
                return  # Exit the function when the destination is reached

            # Update the object's coordinates
            self.x = x
            self.y = y

            # Delay for a short duration to control the rate of object movement
            time.sleep(0.05)