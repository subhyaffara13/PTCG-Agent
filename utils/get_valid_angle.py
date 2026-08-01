
def get_valid_angle(randomizer):
    # generates an angle in [0, 2*np.pi) that
    # excludes (90 +- ver_deg_range), (270 +- ver_deg_range), (0 +- hor_deg_range), (180 +- hor_deg_range)
    # (65, 115), (245, 295), (170, 190), (0, 10), (350, 360)
    ver_deg_range = 25
    hor_deg_range = 10
    a1 = deg_to_rad(90 - ver_deg_range)
    b1 = deg_to_rad(90 + ver_deg_range)
    a2 = deg_to_rad(270 - ver_deg_range)
    b2 = deg_to_rad(270 + ver_deg_range)
    c1 = deg_to_rad(180 - hor_deg_range)
    d1 = deg_to_rad(180 + hor_deg_range)
    c2 = deg_to_rad(360 - hor_deg_range)
    d2 = deg_to_rad(0 + hor_deg_range)

    angle = 0
    while (
        (a1 < angle < b1)
        or (a2 < angle < b2)
        or (c1 < angle < d1)
        or (angle > c2)
        or (angle < d2)
    ):
        angle = 2 * np.pi * randomizer.random()

    return angle

