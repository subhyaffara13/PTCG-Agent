
def choose_colorbrewer_palette(data_type, as_cmap=False):
    """Select a palette from the ColorBrewer set.

    These palettes are built into matplotlib and can be used by name in
    many seaborn functions, or by passing the object returned by this function.

    Parameters
    ----------
    data_type : {'sequential', 'diverging', 'qualitative'}
        This describes the kind of data you want to visualize. See the seaborn
        color palette docs for more information about how to choose this value.
        Note that you can pass substrings (e.g. 'q' for 'qualitative.

    as_cmap : bool
        If True, the return value is a matplotlib colormap rather than a
        list of discrete colors.

    Returns
    -------
    pal or cmap : list of colors or matplotlib colormap
        Object that can be passed to plotting functions.

    See Also
    --------
    dark_palette : Create a sequential palette with dark low values.
    light_palette : Create a sequential palette with bright low values.
    diverging_palette : Create a diverging palette from selected colors.
    cubehelix_palette : Create a sequential palette or colormap using the
                        cubehelix system.


    """
    if data_type.startswith("q") and as_cmap:
        raise ValueError("Qualitative palettes cannot be colormaps.")

    pal = []
    if as_cmap:
        cmap = _init_mutable_colormap()

    if data_type.startswith("s"):
        opts = ["Greys", "Reds", "Greens", "Blues", "Oranges", "Purples",
                "BuGn", "BuPu", "GnBu", "OrRd", "PuBu", "PuRd", "RdPu", "YlGn",
                "PuBuGn", "YlGnBu", "YlOrBr", "YlOrRd"]
        variants = ["regular", "reverse", "dark"]

        @interact
        def choose_sequential(name=opts, n=(2, 18),
                              desat=FloatSlider(min=0, max=1, value=1),
                              variant=variants):
            if variant == "reverse":
                name += "_r"
            elif variant == "dark":
                name += "_d"

            if as_cmap:
                colors = color_palette(name, 256, desat)
                _update_lut(cmap, np.c_[colors, np.ones(256)])
                _show_cmap(cmap)
            else:
                pal[:] = color_palette(name, n, desat)
                palplot(pal)

    elif data_type.startswith("d"):
        opts = ["RdBu", "RdGy", "PRGn", "PiYG", "BrBG",
                "RdYlBu", "RdYlGn", "Spectral"]
        variants = ["regular", "reverse"]

        @interact
        def choose_diverging(name=opts, n=(2, 16),
                             desat=FloatSlider(min=0, max=1, value=1),
                             variant=variants):
            if variant == "reverse":
                name += "_r"
            if as_cmap:
                colors = color_palette(name, 256, desat)
                _update_lut(cmap, np.c_[colors, np.ones(256)])
                _show_cmap(cmap)
            else:
                pal[:] = color_palette(name, n, desat)
                palplot(pal)

    elif data_type.startswith("q"):
        opts = ["Set1", "Set2", "Set3", "Paired", "Accent",
                "Pastel1", "Pastel2", "Dark2"]

        @interact
        def choose_qualitative(name=opts, n=(2, 16),
                               desat=FloatSlider(min=0, max=1, value=1)):
            pal[:] = color_palette(name, n, desat)
            palplot(pal)

    if as_cmap:
        return cmap
    return pal

