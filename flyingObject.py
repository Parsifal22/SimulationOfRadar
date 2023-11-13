import tkinter as tk
import re
import uuid
import time
import random
import math

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

        # Validate and set the angle
        self._set_angle()

    def _set_angle(self):
        # Calculate angle based on direction vector
        if self.x == 0 and self.y == 0:
            self.angle = 0
        else:
            self.angle = math.atan2(self.y, self.x)

        # Convert negative angles to positive
        if self.angle < 0:
            self.angle += 2 * math.pi

    def move(self):
        # Move the object based on speed and angle
        dx = self.speed * math.cos(self.angle)
        dy = self.speed * math.sin(self.angle)
        self.x += dx
        self.y += dy

        # Move the object on the canvas
        self.canvas.coords(self.object_id, self.x - 5, self.y - 5, self.x + 5, self.y + 5)

        # Check expiration time
        current_time = time.time()
        if current_time - self.created_time >= self.expire_time:
            # Delete the object from the canvas
            self.canvas.delete(self.object_id)
        else:
            # Call this function again after a delay for continuous movement
            self.canvas.after(50, self.move)