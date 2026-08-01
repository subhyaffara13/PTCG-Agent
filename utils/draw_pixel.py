
def draw_pixel(surf, pos, color, bright, blend=True):
    """draw one blended pixel with given brightness."""
    try:
        other_col = surf.get_at(pos) if blend else (0, 0, 0, 0)
    except IndexError:  # pixel outside the surface
        return
    new_color = tuple(
        (bright * col + (1 - bright) * pix) for col, pix in zip(color, other_col)
    )
    # FIXME what should happen if only one, color or surf_col, has alpha?
    surf.set_at(pos, new_color)

