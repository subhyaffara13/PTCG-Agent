
def _convert_colors(colors):
    """Convert either a list of colors or nested lists of colors to RGB."""
    to_rgb = mpl.colors.to_rgb

    try:
        to_rgb(colors[0])
        # If this works, there is only one level of colors
        return list(map(to_rgb, colors))
    except ValueError:
        # If we get here, we have nested lists
        return [list(map(to_rgb, color_list)) for color_list in colors]

