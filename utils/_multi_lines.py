
def _multi_lines(
    surf,
    color,
    closed,  # pylint: disable=too-many-arguments
    points,
    width=1,
    blend=False,
    aaline=False,
):
    """draw several lines, either anti-aliased or not."""
    # The code for anti-aliased or not is almost identical, so it's factorized
    if len(points) <= 2:
        raise TypeError
    line = [0] * 4  # store x1, y1 & x2, y2 of the lines to be drawn

    xlist = [pt[0] for pt in points]
    ylist = [pt[1] for pt in points]
    line[0] = xlist[0]
    line[1] = ylist[0]
    b_box = BoundingBox(left=xlist[0], right=xlist[0], top=ylist[0], bottom=ylist[0])

    for line_x, line_y in points[1:]:
        b_box.left = min(b_box.left, line_x)
        b_box.right = max(b_box.right, line_x)
        b_box.top = min(b_box.top, line_y)
        b_box.bottom = max(b_box.bottom, line_y)

    rect = surf.get_clip()
    for loop in range(1, len(points)):
        line[0] = xlist[loop - 1]
        line[1] = ylist[loop - 1]
        line[2] = xlist[loop]
        line[3] = ylist[loop]
        if aaline:
            _clip_and_draw_aaline(surf, rect, color, line, blend)
        else:
            _clip_and_draw_line_width(surf, rect, color, line, width)

    if closed:
        line[0] = xlist[len(points) - 1]
        line[1] = ylist[len(points) - 1]
        line[2] = xlist[0]
        line[3] = ylist[0]
        if aaline:
            _clip_and_draw_aaline(surf, rect, color, line, blend)
        else:
            _clip_and_draw_line_width(surf, rect, color, line, width)

