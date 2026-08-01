
def _draw_aaline(surf, color, start, end, blend):
    """draw an anti-aliased line.

    The algorithm yields identical results with _draw_line for horizontal,
    vertical or diagonal lines, and results changes smoothly when changing
    any of the endpoint coordinates.

    Note that this yields strange results for very short lines, eg
    a line from (0, 0) to (0, 1) will draw 2 pixels, and a line from
    (0, 0) to (0, 1.1) will blend 10 % on the pixel (0, 2).
    """
    # The different requirements that we have on an antialiasing algorithm
    # implies to make some compromises:
    # 1. We want smooth evolution wrt to the 4 endpoint coordinates
    #    (this means also that we want a smooth evolution when the angle
    #     passes +/- 45°
    # 2. We want the same behavior when swapping the endpoints
    # 3. We want understandable results for the endpoint values
    #    (eg we want to avoid half-integer values to draw a simple plain
    #     horizontal or vertical line between two integer l endpoints)
    #
    # This implies to somehow make the line artificially 1 pixel longer
    # and to draw a full pixel when we have the  endpoints are identical.
    d_x = end.x - start.x
    d_y = end.y - start.y

    if d_x == 0 and d_y == 0:
        # For smoothness reasons, we could also do some blending here,
        # but it seems overshoot...
        set_at(surf, int(start.x), int(start.y), color)
        return

    if start.x > end.x or start.y > end.y:
        start.x, end.x = end.x, start.x
        start.y, end.y = end.y, start.y
        d_x = -d_x
        d_y = -d_y

    if abs(d_x) >= abs(d_y):
        slope = d_y / d_x

        def draw_two_pixel(in_x, float_y, factor):
            flr_y = floor(float_y)
            draw_pixel(surf, (in_x, flr_y), color, factor * inv_frac(float_y), blend)
            draw_pixel(surf, (in_x, flr_y + 1), color, factor * frac(float_y), blend)

        _draw_aaline_dx(d_x, slope, end, start, draw_two_pixel)
    else:
        slope = d_x / d_y

        def draw_two_pixel(float_x, in_y, factor):
            fl_x = floor(float_x)
            draw_pixel(surf, (fl_x, in_y), color, factor * inv_frac(float_x), blend)
            draw_pixel(surf, (fl_x + 1, in_y), color, factor * frac(float_x), blend)

        _draw_aaline_dy(d_y, slope, end, start, draw_two_pixel)

