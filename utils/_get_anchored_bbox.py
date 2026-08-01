
def _get_anchored_bbox(loc, bbox, parentbbox, pad_x, pad_y):
    """
    Return the (x, y) position of the *bbox* anchored at the *parentbbox* with
    the *loc* code with the *borderpad* and padding *pad_x*, *pad_y*.
    """
    # This is only called internally and *loc* should already have been
    # validated.  If 0 (None), we just let ``bbox.anchored`` raise.
    c = [None, "NE", "NW", "SW", "SE", "E", "W", "E", "S", "N", "C"][loc]
    container = parentbbox.padded(-pad_x, -pad_y)
    return bbox.anchored(c, container=container).p0

