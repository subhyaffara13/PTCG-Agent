
def _init_mutable_colormap():
    """Create a matplotlib colormap that will be updated by the widgets."""
    greys = color_palette("Greys", 256)
    cmap = LinearSegmentedColormap.from_list("interactive", greys)
    cmap._init()
    cmap._set_extremes()
    return cmap

