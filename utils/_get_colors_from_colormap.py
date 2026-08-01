
def _get_colors_from_colormap(
    colormap: str | Colormap,
    num_colors: int,
) -> list[Color]:
    """Get colors from colormap."""
    cmap = _get_cmap_instance(colormap)
    return [cmap(num) for num in np.linspace(0, 1, num=num_colors)]

