import tkinter as tk
from tkinter import ttk

time_value = 0
objects_value = 0
# Create a function to open the settings window
def openSettings(window):
    # Create a new window for settings
    settings_window = tk.Toplevel(window)
    settings_window.title("Settings")

    # Label and entry for setting simulation time
    time_label = ttk.Label(settings_window, text="Simulation Time (seconds):")
    time_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

    time_entry = ttk.Entry(settings_window)
    time_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    # Label and entry for setting number of objects
    num_objects_label = ttk.Label(settings_window, text="Number of Objects:")
    num_objects_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

    num_objects_entry = ttk.Entry(settings_window)
    num_objects_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

    # Create a button to apply the settings
    apply_button = ttk.Button(settings_window, text="Apply", command=lambda: setValues(time_entry, num_objects_entry))
    apply_button.grid(row=2, column=0, columnspan=2, pady=10)

# Function to set time_value and objects_value
def setValues(time_entry, num_objects_entry):
    global time_value
    global objects_value
    print(time_value)
    time_value = int(time_entry.get()) if time_entry.get().isdigit() else time_value
    objects_value = int(num_objects_entry.get()) if num_objects_entry.get().isdigit() else objects_value
