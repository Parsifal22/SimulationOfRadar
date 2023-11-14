import random
import time
from flyingObject import FlyingObject
from utils import SimulationParameters, determine_sector, calculate_distance
from datetime import timedelta
import threading
import tkinter as tk
import os


# List to store flying objects created during the simulation
simulation_objects = {}

# Function to get the current simulation time
def get_simulation_time(start_time, elapsed_time):
    return start_time + timedelta(seconds=elapsed_time)


# Function to update the timer label
def update_timer(timer_label, start_time, elapsed_time, real_to_sim_time_ratio):
    current_simulation_time = get_simulation_time(start_time, elapsed_time)
    simulated_time_increment = timedelta(seconds=real_to_sim_time_ratio)
    current_simulation_time += simulated_time_increment

    formatted_time = current_simulation_time.strftime('%Y-%m-%d %H:%M:%S')
    timer_label.config(text=f"Timer: {formatted_time}")
    timer_label.after(1000, update_timer, timer_label, start_time, elapsed_time + real_to_sim_time_ratio,
                      real_to_sim_time_ratio)
def clear_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.truncate()



# List to store thread instances
threads = []
# Function to run the simulation for a single FlyingObject
def run_flying_object(window, canvas, start_timeframe, screen_width, screen_height):


    # Generate random coordinates for the initial point
    x, y = None, None
    while x is None or y is None or not (0 <= x <= 1000) or not (
            0 <= y <= 1000) or determine_sector(x, y) is None:
        x = random.uniform(0, screen_width)
        y = random.uniform(0, screen_height)

    # Create a point on the canvas to represent the FlyingObject
    point = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", outline="red")

    flying_object = FlyingObject(
        canvas, x, y, speed=random.uniform(10, 80),
        time_frame=start_timeframe
    )

    # Store the FlyingObject's ID in the point object's tag
    canvas.itemconfig(point, tags=(flying_object.object_id,))

    # Generate random coordinates for the way point
    way_x, way_y = None, None
    while way_x is None or way_y is None or not (
            100 <= calculate_distance(x, y, way_x, way_y) <= 150) or determine_sector(
            way_x, way_y) is None:
        way_x = random.uniform(0, screen_width)
        way_y = random.uniform(0, screen_height)

    # Create a way point on the canvas
    way_point = canvas.create_oval(way_x - 5, way_y - 5, way_x + 5, way_y + 5,
                                             fill="green", outline="green")

    # Generate random coordinates for the destination point
    dest_x, dest_y = None, None
    while dest_x is None or dest_y is None or not (
            150 <= calculate_distance(x, y, dest_x, dest_y) <= 400) or determine_sector(
        dest_x, dest_y) is None:
        dest_x = random.uniform(0, screen_width)
        dest_y = random.uniform(0, screen_height)

    # Create a destination point on the canvas
    dest_point = canvas.create_oval(dest_x - 5, dest_y - 5, dest_x + 5, dest_y + 5,
                                              fill="blue", outline="blue")



    bezier_curve = (x, y, way_x, way_y, dest_x, dest_y)
    canvas.create_line(bezier_curve, smooth="true", tags=flying_object.object_id)

    flying_object.move(dest_x=dest_x, dest_y=dest_y, bezier_curve=bezier_curve)

    # Object has reached the destination, delete it from the canvas
    canvas.delete(flying_object.object_id)
    canvas.delete(dest_point)
    canvas.delete(way_point)


# Create a function to start the simulation
def startSimulation(canvas, window, screen_width, screen_height, start_button):
    start_button['state'] = 'disabled'

    clear_json_file("data.json")

    # Set the arbitrary start date and time (1st of December 2006 at 13:00)
    start_timeframe = SimulationParameters(2006, 12, 1, 13, 0)

    # Generate flying objects randomly for 3 minutes
    end_time = time.time() + 60  # 1 minute
    # Set the ratio of real-time to simulated time (adjust as needed)
    real_to_sim_time_ratio = 10 * 6  # 10 minutes of real-time corresponds to 10 hours of simulated time
    # Create a label for the timer
    timer_label = tk.Label(window, text="Current Time: 00:00:00", font=("Helvetica", 14))
    timer_label.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)
    timer_label.place(x=screen_width - 280, y=screen_height - 75)

    elapsed_time = 0
    # Generate flying objects randomly for 3 minutes
    end_time = time.time() + 60  # 1 minute



    # Start updating the timer label
    update_timer(timer_label, start_timeframe.simulation_start_time, 0, real_to_sim_time_ratio)

    while time.time() < end_time:

        # Calculate the current simulation time
        current_simulation_time = get_simulation_time(start_timeframe.simulation_start_time, elapsed_time)

        # Create a thread for each FlyingObject
        thread = threading.Thread(target=run_flying_object, args=(window, canvas, start_timeframe, screen_width, screen_height))
        threads.append(thread)

        # Start the thread
        thread.start()

        # Increase elapsed time
        elapsed_time += 1

        # Update the canvas
        window.update_idletasks()
        window.update()

        # Sleep for a short duration to control the rate of object creation
        time.sleep(1)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Destroy the timer label after simulation ends
    timer_label.destroy()
    # Enable the button after simulation ends
    start_button['state'] = 'normal'
