
def _draw_aaline_dx(d_x, slope, end, start, draw_two_pixel):
    # A and G are respectively left and right to the "from" point, but
    # with integer-x-coordinate, (and only if from_x is not integer).
    # Hence they appear in following order on the line in general case:
    #  A   from-pt    G    .  .  .        to-pt    S
    #  |------*-------|--- .  .  . ---|-----*------|-
    g_x = ceil(start.x)
    g_y = start.y + (g_x - start.x) * slope
    # 1. Draw start of the segment if we have a non-integer-part
    if start.x < g_x:
        # this corresponds to the point "A"
        draw_two_pixel(floor(start.x), g_y - slope, inv_frac(start.x))
    # 2. Draw end of the segment: we add one pixel for homogeneity reasons
    rest = frac(end.x)
    s_x = ceil(end.x)
    if rest > 0:
        # Again we draw only if we have a non-integer-part
        s_y = start.y + slope * (d_x + 1 - rest)
        draw_two_pixel(s_x, s_y, rest)
    else:
        s_x += 1
    # 3. loop for other points
    for line_x in range(g_x, s_x):
        line_y = g_y + slope * (line_x - g_x)
        draw_two_pixel(line_x, line_y, 1)

