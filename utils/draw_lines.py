
def draw_lines(surf, color, closed, points, width=1):
    """draw several lines connected through the points."""
    return _multi_lines(surf, color, closed, points, width, aaline=False)

