import tkinter as tk
from start_simulation import startSimulation
import threading
from utils import SimulationParameters
from open_settings import openSettings
from rest_api import run_flask_app
from multiprocessing import Process

# Create the main window
window = tk.Tk()
window.title("Simulation of flying objects")

# Get the user's screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window's size
window.geometry(f"{screen_width}x{screen_height}")

# Create a canvas to represent "The World"
canvas = tk.Canvas(window, width=screen_width, height=screen_height, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Initsialize initial parameters
parameters = SimulationParameters()

# Create the "Settings" button
settings_button = tk.Button(window, text="Settings", command=lambda: openSettings(window, parameters))
settings_button.pack(side=tk.LEFT, padx=10)

# Create the "Start simulation" button
start_button = tk.Button(window, text="Start simulation",
                         command=lambda: threading.Thread(target=startSimulation,
                                                          args=(canvas, window, screen_width, screen_height,
                                                                start_button, settings_button, parameters)).start())
start_button.pack(side=tk.LEFT, padx=10)



# Place the "Settings" button next to the "Start simulation" button
canvas.create_window(5, 70, anchor=tk.NW, window=settings_button, width=110, height=50)

# Place the "Start simulation" button at the upper left corner
canvas.create_window(5, 10, anchor=tk.NW, window=start_button, width=110, height=50)

# Function to run the Tkinter main event loop
def run_mainloop():
    window.mainloop()

if __name__ == '__main__':
    # Start the Flask app in a separate process
    flask_process = Process(target=run_flask_app)
    flask_process.start()

    try:
        # Run the Tkinter main event loop in the main thread
        run_mainloop()
    finally:
        flask_process.terminate()
        flask_process.join()



