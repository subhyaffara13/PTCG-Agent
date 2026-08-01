
def _line_t_of_pt(s, e, pt):
    sx, sy = s
    ex, ey = e
    px, py = pt
    if abs(sx - ex) < epsilon and abs(sy - ey) < epsilon:
        # Line is a point!
        return -1
    # Use the largest
    if abs(sx - ex) > abs(sy - ey):
        return (px - sx) / (ex - sx)
    else:
        return (py - sy) / (ey - sy)

