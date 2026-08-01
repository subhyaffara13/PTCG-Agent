
def f_with_problematic_points(x_arr, points, xp):
    """
    This emulates a function with a list of singularities given by `points`.

    If no `x_arr` are one of the `points`, then this function returns 1.
    """

    for point in points:
        if xp.any(x_arr == point):
            raise ValueError("called with a problematic point")

    return xp.ones(x_arr.shape[0])

