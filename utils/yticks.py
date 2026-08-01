
def yticks(
    ticks: ArrayLike | None = None,
    labels: Sequence[str] | None = None,
    *,
    minor: bool = False,
    **kwargs
) -> tuple[list[Tick] | np.ndarray, list[Text]]:
    """
    Get or set the current tick locations and labels of the y-axis.

    Pass no arguments to return the current values without modifying them.

    Parameters
    ----------
    ticks : array-like, optional
        The list of ytick locations.  Passing an empty list removes all yticks.
    labels : array-like, optional
        The labels to place at the given *ticks* locations.  This argument can
        only be passed if *ticks* is passed as well.
    minor : bool, default: False
        If ``False``, get/set the major ticks/labels; if ``True``, the minor
        ticks/labels.
    **kwargs
        `.Text` properties can be used to control the appearance of the labels.

        .. warning::

            This only sets the properties of the current ticks, which is
            only sufficient if you either pass *ticks*, resulting in a
            fixed list of ticks, or if the plot is static.

            Ticks are not guaranteed to be persistent. Various operations
            can create, delete and modify the Tick instances. There is an
            imminent risk that these settings can get lost if you work on
            the figure further (including also panning/zooming on a
            displayed figure).

            Use `~.pyplot.tick_params` instead if possible.

    Returns
    -------
    locs
        The list of ytick locations.
    labels
        The list of ylabel `.Text` objects.

    Notes
    -----
    Calling this function with no arguments (e.g. ``yticks()``) is the pyplot
    equivalent of calling `~.Axes.get_yticks` and `~.Axes.get_yticklabels` on
    the current Axes.
    Calling this function with arguments is the pyplot equivalent of calling
    `~.Axes.set_yticks` and `~.Axes.set_yticklabels` on the current Axes.

    Examples
    --------
    >>> locs, labels = yticks()  # Get the current locations and labels.
    >>> yticks(np.arange(0, 1, step=0.2))  # Set label locations.
    >>> yticks(np.arange(3), ['Tom', 'Dick', 'Sue'])  # Set text labels.
    >>> yticks([0, 1, 2], ['January', 'February', 'March'],
    ...        rotation=45)  # Set text labels and properties.
    >>> yticks([])  # Disable yticks.
    """
    ax = gca()

    locs: list[Tick] | np.ndarray
    if ticks is None:
        locs = ax.get_yticks(minor=minor)
        if labels is not None:
            raise TypeError("yticks(): Parameter 'labels' can't be set "
                            "without setting 'ticks'")
    else:
        locs = ax.set_yticks(ticks, minor=minor)

    labels_out: list[Text] = []
    if labels is None:
        labels_out = ax.get_yticklabels(minor=minor)
        for l in labels_out:
            l._internal_update(kwargs)
    else:
        labels_out = ax.set_yticklabels(labels, minor=minor, **kwargs)

    return locs, labels_out

