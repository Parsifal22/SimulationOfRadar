import tkinter as tk
from tkinter import ttk

hours_value = 1
object_value = 40

# Create a function to open the settings window
def openSettings(window, parameters):
    # Create a new window for settings
    settings_window = tk.Toplevel(window)
    settings_window.title("Settings")

    # Label and entry for setting simulation time (hours)
    hours_label = ttk.Label(settings_window, text="Hours:")
    hours_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

    hours_entry = ttk.Entry(settings_window)
    hours_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)


    # Line to separate sections
    ttk.Separator(settings_window, orient=tk.HORIZONTAL).grid(row=3, columnspan=2, sticky="ew", pady=10)

    # Label and entry for setting the number of objects
    objects_label = ttk.Label(settings_window, text="Number of Objects:")
    objects_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

    objects_entry = ttk.Entry(settings_window)
    objects_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

    # Create a button to apply the settings
    apply_button = ttk.Button(settings_window, text="Apply", command=lambda: setValues(hours_entry, objects_entry, parameters, settings_window))
    apply_button.grid(row=2, column=0, columnspan=2, pady=10)


# Function to set hours_value, minutes_value, seconds_value, and objects_value
def setValues(hours_entry, objects_entry, parameters, window):
    global hours_value, objects_value
    # Get the entry values
    hours_str = hours_entry.get()
    objects_str = objects_entry.get()

    # Convert time values to seconds
    hours_value = int(hours_str) * 3600 if hours_str.isdigit() else hours_value

    # Calculate the total time in seconds
    total_seconds = hours_value

    # Update the objects_value
    objects_value = int(objects_str) if objects_str.isdigit() else objects_value

    parameters.set_duration(total_seconds)
    parameters.set_objects(objects_value)

    # Close the settings window
    window.destroy()
