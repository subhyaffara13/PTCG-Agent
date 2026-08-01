
def matshow(A: ArrayLike, fignum: None | int = None, **kwargs) -> AxesImage:
    """
    Display a 2D array as a matrix in a new figure window.

    The origin is set at the upper left hand corner.
    The indexing is ``(row, column)`` so that the first index runs vertically
    and the second index runs horizontally in the figure:

    .. code-block:: none

        A[0, 0]   ⋯ A[0, M-1]
           ⋮             ⋮
        A[N-1, 0] ⋯ A[N-1, M-1]

    The aspect ratio of the figure window is that of the array,
    unless this would make an excessively short or narrow figure.

    Tick labels for the xaxis are placed on top.

    Parameters
    ----------
    A : 2D array-like
        The matrix to be displayed.

    fignum : None or int
        If *None*, create a new, appropriately sized figure window.

        If 0, use the current Axes (creating one if there is none, without ever
        adjusting the figure size).

        Otherwise, create a new Axes on the figure with the given number
        (creating it at the appropriate size if it does not exist, but not
        adjusting the figure size otherwise).  Note that this will be drawn on
        top of any preexisting Axes on the figure.

    Returns
    -------
    `~matplotlib.image.AxesImage`

    Other Parameters
    ----------------
    **kwargs : `~matplotlib.axes.Axes.imshow` arguments

    """
    A = np.asanyarray(A)
    if fignum == 0:
        ax = gca()
    else:
        if fignum is not None and fignum_exists(fignum):
            # Do not try to set a figure size.
            figsize = None
        else:
            # Extract actual aspect ratio of array and make appropriately sized figure.
            figsize = figaspect(A)
        fig = figure(fignum, figsize=figsize)
        ax = fig.add_axes((0.15, 0.09, 0.775, 0.775))
    im = ax.matshow(A, **kwargs)
    sci(im)
    return im

