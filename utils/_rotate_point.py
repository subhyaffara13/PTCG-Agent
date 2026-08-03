import math


def _rotate_point(angle, x, y):
    """
    Rotate point (x, y) by rotation angle in degrees
    """
    if angle == 0:
        return (x, y)
    angle_rad = math.radians(angle)
    cos, sin = math.cos(angle_rad), math.sin(angle_rad)
    return (cos * x - sin * y, sin * x + cos * y)

