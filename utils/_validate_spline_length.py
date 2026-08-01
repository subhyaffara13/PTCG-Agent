
def _validate_spline_length(spline):
    if len(spline) < 3:
        raise ValueError("Quadratic splines must contain at least 3 points")

