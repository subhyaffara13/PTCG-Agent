
def _get_cmap_instance(colormap: str | Colormap) -> Colormap:
    """Get instance of matplotlib colormap."""
    if isinstance(colormap, str):
        cmap = colormap
        colormap = mpl.colormaps[colormap]
        if colormap is None:
            raise ValueError(f"Colormap {cmap} is not recognized")
    return colormap

