
def _point_pair_length(point_1, point_2):
    """The length of the direct linear path between two points."""
    return _point_pair_relative_position(point_1, point_2).magnitude()

