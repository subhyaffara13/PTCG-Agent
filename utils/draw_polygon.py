
def draw_polygon(surface, color, points, width):
    """Draw a polygon"""
    if width:
        draw_lines(surface, color, 1, points, width)
        return  # TODO Rect(...)
    num_points = len(points)
    point_x = [x for x, y in points]
    point_y = [y for x, y in points]

    miny = min(point_y)
    maxy = max(point_y)

    if miny == maxy:
        minx = min(point_x)
        maxx = max(point_x)
        _clip_and_draw_horizline(surface, color, minx, miny, maxx)
        return  # TODO Rect(...)

    for y_coord in range(miny, maxy + 1):
        x_intersect = []
        for i in range(num_points):
            _draw_polygon_inner_loop(i, point_x, point_y, y_coord, x_intersect)

        x_intersect.sort()
        for i in range(0, len(x_intersect), 2):
            _clip_and_draw_horizline(
                surface, color, x_intersect[i], y_coord, x_intersect[i + 1]
            )

    # special case : horizontal border lines
    for i in range(num_points):
        i_prev = i - 1 if i else num_points - 1
        if miny < point_y[i] == point_y[i_prev] < maxy:
            _clip_and_draw_horizline(
                surface, color, point_x[i], point_y[i], point_x[i_prev]
            )

    return  # TODO Rect(...)

