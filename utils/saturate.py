
def saturate(color):
    """Return a fully saturated color with the same hue.

    Parameters
    ----------
    color : matplotlib color
        hex, rgb-tuple, or html color name

    Returns
    -------
    new_color : rgb tuple
        saturated color code in RGB tuple representation

    """
    return set_hls_values(color, s=1)

