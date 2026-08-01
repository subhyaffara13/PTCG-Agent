
def split_points_by_offsets(
    points: cpy.PointArray,
    offsets: cpy.OffsetArray,
) -> list[cpy.PointArray]:
    """Split a point array at locations specified by an offset array into a list of point arrays.
    """
    check_point_array(points)
    check_offset_array(offsets)

    if len(offsets) > 2:
        return np.split(points, offsets[1:-1])
    else:
        return [points]

