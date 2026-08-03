import math


def _polar(r, theta_deg):
    theta = math.radians(theta_deg)
    return r * math.cos(theta), r * math.sin(theta)

