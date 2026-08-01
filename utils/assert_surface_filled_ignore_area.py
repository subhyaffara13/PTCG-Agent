
def assertSurfaceFilledIgnoreArea(testcase, surface, expected_color, ignore_rect):
    """Checks if the surface is filled with the given color. The
    ignore_rect area is not checked.
    """
    x_range = range(surface.get_width())
    y_range = range(surface.get_height())
    ignore_rect.normalize()

    surface.lock()  # Lock for possible speed up.
    for pos in ((x, y) for y in y_range for x in x_range):
        if not ignore_rect.collidepoint(pos):
            testcase.assertEqual(surface.get_at(pos), expected_color, pos)
    surface.unlock()

