
def _draw_line(surf, color, start, end):
    """draw a non-horizontal line (without anti-aliasing)."""
    # Variant of https://en.wikipedia.org/wiki/Bresenham's_line_algorithm
    #
    # This strongly differs from craw.c implementation, because we use a
    # "slope" variable (instead of delta_x and delta_y) and a "error" variable.
    # And we can not do pointer-arithmetic with "BytesPerPixel", like in
    # the C-algorithm.
    if start.x == end.x:
        # This case should not happen...
        raise ValueError

    slope = abs((end.y - start.y) / (end.x - start.x))
    error = 0.0

    if slope < 1:
        # Here, it's a rather horizontal line

        # 1. check in which octants we are & set init values
        if end.x < start.x:
            start.x, end.x = end.x, start.x
            start.y, end.y = end.y, start.y
        line_y = start.y
        dy_sign = 1 if (start.y < end.y) else -1

        # 2. step along x coordinate
        for line_x in range(start.x, end.x + 1):
            set_at(surf, line_x, line_y, color)
            error += slope
            if error >= 0.5:
                line_y += dy_sign
                error -= 1
    else:
        # Case of a rather vertical line

        # 1. check in which octants we are & set init values
        if start.y > end.y:
            start.x, end.x = end.x, start.x
            start.y, end.y = end.y, start.y
        line_x = start.x
        slope = 1 / slope
        dx_sign = 1 if (start.x < end.x) else -1

        # 2. step along y coordinate
        for line_y in range(start.y, end.y + 1):
            set_at(surf, line_x, line_y, color)
            error += slope
            if error >= 0.5:
                line_x += dx_sign
                error -= 1


def _draw_line(buf: list[list[Color | None]], x0: int, y0: int, x1: int, y1: int, color: Color) -> None:
    bh = len(buf)
    bw = len(buf[0]) if buf else 0
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    steps = max(dx, dy)
    if steps == 0:
        if 0 <= y0 < bh and 0 <= x0 < bw:
            buf[y0][x0] = color
        return
    xi = (x1 - x0) / steps
    yi = (y1 - y0) / steps
    fx, fy = float(x0), float(y0)
    for _ in range(steps + 1):
        px, py = round(fx), round(fy)
        if 0 <= py < bh and 0 <= px < bw:
            buf[py][px] = color
        fx += xi
        fy += yi

