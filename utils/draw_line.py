
def draw_line(surf, color, from_point, to_point, width=1):
    """draw anti-aliased line between two endpoints."""
    line = [from_point[0], from_point[1], to_point[0], to_point[1]]
    return _clip_and_draw_line_width(surf, surf.get_clip(), color, line, width)

