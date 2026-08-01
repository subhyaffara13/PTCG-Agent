
def _clip_and_draw_aaline(surf, rect, color, line, blend):
    """draw anti-aliased line between two endpoints."""
    if not clip_line(
        line,
        BoundingBox(rect.x - 1, rect.y - 1, rect.x + rect.w, rect.y + rect.h),
        use_float=True,
    ):
        return  # TODO Rect(rect.x, rect.y, 0, 0)
    _draw_aaline(surf, color, Point(line[0], line[1]), Point(line[2], line[3]), blend)
    return  # TODO Rect(-- affected area --)

