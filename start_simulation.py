import random
import time
from flyingObject import FlyingObject
from math import hypot

# List to store flying objects created during the simulation
simulation_objects = {}

# Function to calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    return hypot(x2 - x1, y2 - y1)

# Create a function to start the simulation
def startSimulation(canvas, screen_width, screen_height, start_button):
    start_button['state'] = 'disabled'

    # Generate flying objects randomly for 3 minutes
    end_time = time.time() + 60  # 1 minute
    while time.time() < end_time:
        # Generate random coordinates for the flying object
        x = random.uniform(0, screen_width)
        y = random.uniform(0, screen_height)

        # Create a FlyingObject on the canvas
        flying_object = FlyingObject(canvas, x, y, speed=random.uniform(10, 80),
                                     payload="0a1b2c3d")

        # Create a point on the canvas to represent the FlyingObject
        point = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", outline="red")

        # Store the FlyingObject's ID in the point object's tag
        canvas.itemconfig(point, tags=(flying_object.object_id,))

        # Store the FlyingObject in the dictionary using object_id as the key
        simulation_objects[flying_object.object_id] = (flying_object, point)

        # Generate random coordinates for the destination point
        way_x, way_y = None, None
        while way_x is None or way_y is None or not (100 <= calculate_distance(x, y, way_x, way_y) <= 150):
            way_x = random.uniform(0, screen_width)
            way_y = random.uniform(0, screen_height)
        # Create a destination point on the canvas
        way_point = canvas.create_oval(way_x - 5, way_y - 5, way_x + 5, way_y + 5, fill="green", outline="green")

        # Generate random coordinates for the destination point
        dest_x, dest_y = None, None
        while dest_x is None or dest_y is None or not (150 <= calculate_distance(x, y, dest_x, dest_y) <= 400):
            dest_x = random.uniform(0, screen_width)
            dest_y = random.uniform(0, screen_height)

        # Create a destination point on the canvas
        dest_point = canvas.create_oval(dest_x - 5, dest_y - 5, dest_x + 5, dest_y + 5, fill="blue", outline="blue")

        # Create a quadratic Bezier curve
        bezier_curve = (x, y, way_x, way_y, dest_x, dest_y)
        canvas.create_line(bezier_curve, smooth="true", tags=flying_object.object_id)

        flying_object.move(dest_x, dest_y, way_x, way_y, bezier_curve)
        # Object has reached the destination, delete it from the canvas
        canvas.delete(flying_object.object_id)
        canvas.delete(dest_point)
        canvas.delete(way_point)
        # Sleep for a short duration to control the rate of object creation
        time.sleep(0.5)

    # Simulation ended, delete all objects
    for object_id, (flying_object, point) in simulation_objects.items():
        canvas.delete(point)

    # Enable the button after simulation ends
    start_button['state'] = 'normal'
