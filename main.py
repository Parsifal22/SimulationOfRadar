import tkinter as tk
from start_simulation import startSimulation
import threading
from open_settings import openSettings

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

# Create the "Start simulation" button
start_button = tk.Button(window, text="Start simulation",
                         command=lambda: threading.Thread(target=startSimulation,
                                                          args=(canvas, window, screen_width, screen_height, start_button)).start())
start_button.pack(side=tk.LEFT, padx=10)

# Place the "Start simulation" button at the upper left corner
canvas.create_window(5, 10, anchor=tk.NW, window=start_button, width=110, height=50)



# Start the main event loop
window.mainloop()
