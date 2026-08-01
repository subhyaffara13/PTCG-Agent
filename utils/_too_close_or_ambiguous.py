
def _too_close_or_ambiguous(x, y, planets):
    """True if (x, y) is too close to any existing planet or sits at a
    Euclidean distance within EPSILON of an integer (which would make the
    ceil-distance platform-dependent).
    """
    for p in planets:
        actual = math.hypot(p[1] - x, p[2] - y)
        if math.ceil(actual) < MIN_DISTANCE:
            return True
        if abs(actual - round(actual)) < EPSILON:
            return True
    return False

