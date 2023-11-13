

# Function to calculate the quadratic Bezier curve coordinates
def quadratic_bezier(t, p0, p1, p2):
    u = 1 - t
    x = u**2 * p0[0] + 2 * u * t * p1[0] + t**2 * p2[0]
    y = u**2 * p0[1] + 2 * u * t * p1[1] + t**2 * p2[1]
    return x, y


