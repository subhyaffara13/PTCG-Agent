
def _point_pair_extension_velocity(point_1, point_2):
    """The extension velocity of the direct linear path between two points."""
    return _point_pair_length(point_1, point_2).diff(dynamicsymbols._t)

