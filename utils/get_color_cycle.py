
def get_color_cycle():
    """Return the list of colors in the current matplotlib color cycle

    Parameters
    ----------
    None

    Returns
    -------
    colors : list
        List of matplotlib colors in the current cycle, or dark gray if
        the current color cycle is empty.
    """
    cycler = mpl.rcParams['axes.prop_cycle']
    return cycler.by_key()['color'] if 'color' in cycler.keys else [".15"]

