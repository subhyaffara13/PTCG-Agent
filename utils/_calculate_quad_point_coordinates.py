
def _calculate_quad_point_coordinates(x, y, width, height, angle=0):
    """
    Calculate the coordinates of rectangle when rotated by angle around x, y
    """

    angle = math.radians(-angle)
    sin_angle = math.sin(angle)
    cos_angle = math.cos(angle)
    a = x + height * sin_angle
    b = y + height * cos_angle
    c = x + width * cos_angle + height * sin_angle
    d = y - width * sin_angle + height * cos_angle
    e = x + width * cos_angle
    f = y - width * sin_angle
    return ((x, y), (e, f), (c, d), (a, b))

