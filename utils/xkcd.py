
def xkcd(
    scale: float = 1, length: float = 100, randomness: float = 2
) -> ExitStack:
    """
    Turn on `xkcd <https://xkcd.com/>`_ sketch-style drawing mode.

    This will only have an effect on things drawn after this function is called.

    For best results, install the `xkcd script <https://github.com/ipython/xkcd-font/>`_
    font; xkcd fonts are not packaged with Matplotlib.

    Parameters
    ----------
    scale : float, optional
        The amplitude of the wiggle perpendicular to the source line.
    length : float, optional
        The length of the wiggle along the line.
    randomness : float, optional
        The scale factor by which the length is shrunken or expanded.

    Notes
    -----
    This function works by a number of rcParams, overriding those set before.

    If you want the effects of this function to be temporary, it can
    be used as a context manager, for example::

        with plt.xkcd():
            # This figure will be in XKCD-style
            fig1 = plt.figure()
            # ...

        # This figure will be in regular style
        fig2 = plt.figure()
    """
    # This cannot be implemented in terms of contextmanager() or rc_context()
    # because this needs to work as a non-contextmanager too.

    if rcParams['text.usetex']:
        raise RuntimeError(
            "xkcd mode is not compatible with text.usetex = True")

    stack = ExitStack()
    stack.callback(rcParams._update_raw, rcParams.copy())

    from matplotlib import patheffects
    rcParams.update({
        'font.family': ['xkcd', 'xkcd Script', 'Comic Neue', 'Comic Sans MS'],
        'font.size': 14.0,
        'path.sketch': (scale, length, randomness),
        'path.effects': [
            patheffects.withStroke(linewidth=4, foreground="w")],
        'axes.linewidth': 1.5,
        'lines.linewidth': 2.0,
        'figure.facecolor': 'white',
        'grid.linewidth': 0.0,
        'axes.grid': False,
        'axes.unicode_minus': False,
        'axes.edgecolor': 'black',
        'xtick.major.size': 8,
        'xtick.major.width': 3,
        'ytick.major.size': 8,
        'ytick.major.width': 3,
    })

    return stack

