
def _update_lut(cmap, colors):
    """Change the LUT values in a matplotlib colormap in-place."""
    cmap._lut[:256] = colors
    cmap._set_extremes()

