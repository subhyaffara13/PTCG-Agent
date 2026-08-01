
def _get_rotate_command(lbrt):
    """Return a PostScript 90° rotation command for bounding box *lbrt*=(l, b, r, t)."""
    l, b, r, t = lbrt
    return f"{l+r:.2f} {0:.2f} translate\n90 rotate"

