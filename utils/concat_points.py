
def concat_points(list_of_points: list[cpy.PointArray]) -> cpy.PointArray:
    """Concatenate a list of point arrays into a single point array.
    """
    if not list_of_points:
        raise ValueError("Empty list passed to concat_points")

    return np.concatenate(list_of_points, dtype=point_dtype)

