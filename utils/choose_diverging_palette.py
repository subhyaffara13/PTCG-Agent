
def choose_diverging_palette(as_cmap=False):
    """Launch an interactive widget to choose a diverging color palette.

    This corresponds with the :func:`diverging_palette` function. This kind
    of palette is good for data that range between interesting low values
    and interesting high values with a meaningful midpoint. (For example,
    change scores relative to some baseline value).

    Requires IPython 2+ and must be used in the notebook.

    Parameters
    ----------
    as_cmap : bool
        If True, the return value is a matplotlib colormap rather than a
        list of discrete colors.

    Returns
    -------
    pal or cmap : list of colors or matplotlib colormap
        Object that can be passed to plotting functions.

    See Also
    --------
    diverging_palette : Create a diverging color palette or colormap.
    choose_colorbrewer_palette : Interactively choose palettes from the
                                 colorbrewer set, including diverging palettes.

    """
    pal = []
    if as_cmap:
        cmap = _init_mutable_colormap()

    @interact
    def choose_diverging_palette(
        h_neg=IntSlider(min=0,
                        max=359,
                        value=220),
        h_pos=IntSlider(min=0,
                        max=359,
                        value=10),
        s=IntSlider(min=0, max=99, value=74),
        l=IntSlider(min=0, max=99, value=50),  # noqa: E741
        sep=IntSlider(min=1, max=50, value=10),
        n=(2, 16),
        center=["light", "dark"]
    ):
        if as_cmap:
            colors = diverging_palette(h_neg, h_pos, s, l, sep, 256, center)
            _update_lut(cmap, colors)
            _show_cmap(cmap)
        else:
            pal[:] = diverging_palette(h_neg, h_pos, s, l, sep, n, center)
            palplot(pal)

    if as_cmap:
        return cmap
    return pal

