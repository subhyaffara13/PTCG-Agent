
def _pair_invalid(x1, y1, x2, y2, planets):
    """Validation for a candidate pair of symmetric planets."""
    a = math.hypot(x1 - x2, y1 - y2)
    if math.ceil(a) < MIN_DISTANCE or abs(a - round(a)) < EPSILON:
        return True
    if _too_close_or_ambiguous(x1, y1, planets):
        return True
    if _too_close_or_ambiguous(x2, y2, planets):
        return True
    return False

