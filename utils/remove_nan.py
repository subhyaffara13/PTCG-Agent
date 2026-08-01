
def remove_nan(points: cpy.PointArray) -> tuple[cpy.PointArray, cpy.OffsetArray]:
    """Remove NaN from a points array, also return the offsets corresponding to the NaN removed.
    """
    check_point_array(points)

    nan_offsets = np.nonzero(np.isnan(points[:, 0]))[0]
    if len(nan_offsets) == 0:
        return points, np.array([0, len(points)], dtype=offset_dtype)
    else:
        points = np.delete(points, nan_offsets, axis=0)
        nan_offsets -= np.arange(len(nan_offsets))
        offsets: cpy.OffsetArray = np.empty(len(nan_offsets)+2, dtype=offset_dtype)
        offsets[0] = 0
        offsets[1:-1] = nan_offsets
        offsets[-1] = len(points)
        return points, offsets

