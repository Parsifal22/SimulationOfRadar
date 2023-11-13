import tkinter as tk
from flyingObject import FlyingObject
import random

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

# Dictionary to store flying objects
flying_objects = {}

# Function to handle mouse clicks on the canvas
def canvas_click(event):
    x = event.x
    y = event.y
    print(f"Clicked at (x={x}, y={y})")

    # Create a FlyingObject on the canvas
    flying_object = FlyingObject(canvas, x, y, speed=random.uniform(1, 10), expire_time=random.uniform(3, 10), payload="0a1b2c3d")

    # Create a point on the canvas to represent the FlyingObject
    point = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", outline="red")

    # Store the FlyingObject's ID in the point object's tag
    canvas.itemconfig(point, tags=(flying_object.object_id,))
    flying_objects[flying_object.object_id] = flying_object
    # Move the FlyingObject
    flying_object.move()


# Variable to store the tooltip reference
tooltip = None


# Function to show FlyingObject info in a tooltip
def show_object_info(event):
    global tooltip

    # Get the tags (object_id) of the hovered item
    tags = canvas.gettags(tk.CURRENT)
    object_id = tags[0] if tags else None

    # Find the FlyingObject with the matching object_id
    if object_id in flying_objects:
        flying_object = flying_objects[object_id]

        # Display object information in a tooltip
        info_str = f"Object ID: {flying_object.object_id}\nSpeed: {flying_object.speed} m/s\nExpire Time: {flying_object.expire_time} seconds"

        # Hide the existing tooltip (if any)
        hide_tooltip()

        # Create and display the tooltip
        tooltip = tk.Toplevel(window)
        tooltip.wm_overrideredirect(True)  # Remove window decorations
        tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")  # Offset from the mouse cursor
        label = tk.Label(tooltip, text=info_str, justify='left')
        label.pack()

        # Schedule the tooltip to disappear after 10 seconds
        window.after(3000, hide_tooltip)


# Function to hide the tooltip
def hide_tooltip():
    global tooltip
    if tooltip:
        tooltip.destroy()
        tooltip = None


# Bind the canvas click event to the function
canvas.bind("<Button-1>", canvas_click)

# Bind the canvas motion event to show_object_info
canvas.bind("<Motion>", show_object_info)

# Start the main event loop
window.mainloop()
