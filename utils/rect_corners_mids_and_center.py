
def rect_corners_mids_and_center(rect):
    """Returns a tuple with each corner, mid, and the center for a given rect.

    Clockwise from the top left corner and ending with the center point.
    """
    return (
        rect.topleft,
        rect.midtop,
        rect.topright,
        rect.midright,
        rect.bottomright,
        rect.midbottom,
        rect.bottomleft,
        rect.midleft,
        rect.center,
    )

