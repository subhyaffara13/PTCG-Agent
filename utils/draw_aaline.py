
def draw_aaline(surf, color, from_point, to_point, blend=True):
    """draw anti-aliased line between two endpoints."""
    line = [from_point[0], from_point[1], to_point[0], to_point[1]]
    return _clip_and_draw_aaline(surf, surf.get_clip(), color, line, blend)

