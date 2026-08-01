
def get_spline_knot_values(order):
    """Knot values to the right of a B-spline's center."""
    knot_values = {0: [1],
                   1: [1],
                   2: [6, 1],
                   3: [4, 1],
                   4: [230, 76, 1],
                   5: [66, 26, 1]}

    return knot_values[order]

