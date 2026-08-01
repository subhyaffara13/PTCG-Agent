
def assertSurfaceFilled(testcase, surface, expected_color, area_rect=None):
    """Checks to see if the given surface is filled with the given color.

    If an area_rect is provided, only check that area of the surface.
    """
    if area_rect is None:
        x_range = range(surface.get_width())
        y_range = range(surface.get_height())
    else:
        area_rect.normalize()
        area_rect = area_rect.clip(surface.get_rect())
        x_range = range(area_rect.left, area_rect.right)
        y_range = range(area_rect.top, area_rect.bottom)

    surface.lock()  # Lock for possible speed up.
    for pos in ((x, y) for y in y_range for x in x_range):
        testcase.assertEqual(surface.get_at(pos), expected_color, pos)
    surface.unlock()

