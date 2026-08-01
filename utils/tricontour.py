
def tricontour(*args, **kwargs):
    __ret = gca().tricontour(*args, **kwargs)
    if __ret._A is not None:  # type: ignore[attr-defined]
        sci(__ret)
    return __ret


def tricontour(ax, *args, **kwargs):
    """
    %(_tricontour_doc)s

    linewidths : float or array-like, default: :rc:`contour.linewidth`
        The line width of the contour lines.

        If a number, all levels will be plotted with this linewidth.

        If a sequence, the levels in ascending order will be plotted with
        the linewidths in the order specified.

        If None, this falls back to :rc:`lines.linewidth`.

    linestyles : {*None*, 'solid', 'dashed', 'dashdot', 'dotted'}, optional
        If *linestyles* is *None*, the default is 'solid' unless the lines are
        monochrome.  In that case, negative contours will take their linestyle
        from :rc:`contour.negative_linestyle` setting.

        *linestyles* can also be an iterable of the above strings specifying a
        set of linestyles to be used. If this iterable is shorter than the
        number of contour levels it will be repeated as necessary.
    """
    kwargs['filled'] = False
    return TriContourSet(ax, *args, **kwargs)

