
def set_cmap(cmap: Colormap | str) -> None:
    """
    Set the default colormap, and applies it to the current image if any.

    Parameters
    ----------
    cmap : `~matplotlib.colors.Colormap` or str
        A colormap instance or the name of a registered colormap.

    See Also
    --------
    colormaps
    get_cmap
    """
    cmap = get_cmap(cmap)

    rc('image', cmap=cmap.name)
    im = gci()

    if im is not None:
        im.set_cmap(cmap)

