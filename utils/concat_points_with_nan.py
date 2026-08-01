
def concat_points_with_nan(list_of_points: list[cpy.PointArray]) -> cpy.PointArray:
    """Concatenate a list of points into a single point array with NaNs used to separate each line.
    """
    if not list_of_points:
        raise ValueError("Empty list passed to concat_points_with_nan")

    if len(list_of_points) == 1:
        return list_of_points[0]
    else:
        nan_spacer = np.full((1, 2), np.nan, dtype=point_dtype)
        list_of_points = [list_of_points[0],
                          *list(chain(*((nan_spacer, x) for x in list_of_points[1:])))]
        return concat_points(list_of_points)

