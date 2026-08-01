
def _color_to_rgb(color, input):
    """Add some more flexibility to color choices."""
    if input == "hls":
        color = colorsys.hls_to_rgb(*color)
    elif input == "husl":
        color = husl.husl_to_rgb(*color)
        color = tuple(np.clip(color, 0, 1))
    elif input == "xkcd":
        color = xkcd_rgb[color]

    return mpl.colors.to_rgb(color)

