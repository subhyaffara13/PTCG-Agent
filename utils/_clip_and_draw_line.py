
def _clip_and_draw_line(surf, rect, color, pts):
    """clip the line into the rectangle and draw if needed.

    Returns true if anything has been drawn, else false."""
    # "pts" is a list with the four coordinates of the two endpoints
    # of the line to be drawn : pts = x1, y1, x2, y2.
    # The data format is like that to stay closer to the C-algorithm.
    if not clip_line(
        pts, BoundingBox(rect.x, rect.y, rect.x + rect.w - 1, rect.y + rect.h - 1)
    ):
        # The line segment defined by "pts" is not crossing the rectangle
        return 0
    if pts[1] == pts[3]:  # eg y1 == y2
        _drawhorzline(surf, color, pts[0], pts[1], pts[2])
    elif pts[0] == pts[2]:  # eg x1 == x2
        _drawvertline(surf, color, pts[0], pts[1], pts[3])
    else:
        _draw_line(surf, color, Point(pts[0], pts[1]), Point(pts[2], pts[3]))
    return 1

