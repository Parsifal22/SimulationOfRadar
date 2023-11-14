import datetime
import threading
import time
from math import hypot

# Function to calculate the quadratic Bezier curve coordinates
def quadratic_bezier(t, p0, p1, p2):
    u = 1 - t
    x = u**2 * p0[0] + 2 * u * t * p1[0] + t**2 * p2[0]
    y = u**2 * p0[1] + 2 * u * t * p1[1] + t**2 * p2[1]
    return x, y


# Function to determine the sector based on coordinates
def determine_sector(x, y):
    if 0 <= x < 500 and 0 <= y < 500:
        return "A"
    elif 500 <= x <= 1000 and 0 <= y < 500:
        return "B"
    elif 0 <= x < 500 and 500 <= y <= 1000:
        return "C"
    elif 500 <= x <= 1000 and 500 <= y <= 1000:
        return "D"
    else:
        return None


# Function to calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    return hypot(x2 - x1, y2 - y1)


class SimulationParameters:
    def __init__(self, start_year, start_month, start_day, start_hour, start_minute):
        self.simulation_start_time = datetime.datetime(start_year, start_month, start_day, start_hour, start_minute)
        self.current_time = self.simulation_start_time
        self.stop_event = threading.Event()
        self.update_thread = threading.Thread(target=self._update_time, daemon=True)
        self.update_thread.start()
    def _update_time(self):
        while not self.stop_event.is_set():
            time.sleep(1)  # Update time every second
            self.current_time += datetime.timedelta(seconds=60)

    def stop_simulation(self):
        self.stop_event.set()
        self.update_thread.join()

    def get_current_time(self):
        return self.current_time
