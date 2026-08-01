
def subplot(nrows: int, ncols: int, index: int, /, **kwargs): ...


def subplot(pos: int | SubplotSpec, /, **kwargs): ...


def subplot(**kwargs): ...


def subplot(*args, **kwargs) -> Axes:
    """
    Add an Axes to the current figure or retrieve an existing Axes.

    This is a wrapper of `.Figure.add_subplot` which provides additional
    behavior when working with the implicit API (see the notes section).

    Call signatures::

       subplot(nrows, ncols, index, **kwargs)
       subplot(pos, **kwargs)
       subplot(**kwargs)

    Parameters
    ----------
    *args : int, (int, int, *index*), or `.SubplotSpec`, default: (1, 1, 1)
        The position of the subplot described by one of

        - Three integers (*nrows*, *ncols*, *index*). The subplot will take the
          *index* position on a grid with *nrows* rows and *ncols* columns.
          *index* starts at 1 in the upper left corner and increases to the
          right. *index* can also be a two-tuple specifying the (*first*,
          *last*) indices (1-based, and including *last*) of the subplot, e.g.,
          ``fig.add_subplot(3, 1, (1, 2))`` makes a subplot that spans the
          upper 2/3 of the figure.
        - A 3-digit integer. The digits are interpreted as if given separately
          as three single-digit integers, i.e. ``fig.add_subplot(235)`` is the
          same as ``fig.add_subplot(2, 3, 5)``. Note that this can only be used
          if there are no more than 9 subplots.
        - A `.SubplotSpec`.

    projection : {None, 'aitoff', 'hammer', 'lambert', 'mollweide', \
'polar', 'rectilinear', str}, optional
        The projection type of the subplot (`~.axes.Axes`). *str* is the name
        of a custom projection, see `~matplotlib.projections`. The default
        None results in a 'rectilinear' projection.

    polar : bool, default: False
        If True, equivalent to projection='polar'.

    sharex, sharey : `~matplotlib.axes.Axes`, optional
        Share the x or y `~matplotlib.axis` with sharex and/or sharey. The
        axis will have the same limits, ticks, and scale as the axis of the
        shared Axes.

    label : str
        A label for the returned Axes.

    Returns
    -------
    `~.axes.Axes`

        The Axes of the subplot. The returned Axes can actually be an instance
        of a subclass, such as `.projections.polar.PolarAxes` for polar
        projections.

    Other Parameters
    ----------------
    **kwargs
        This method also takes the keyword arguments for the returned Axes
        base class; except for the *figure* argument. The keyword arguments
        for the rectilinear base class `~.axes.Axes` can be found in
        the following table but there might also be other keyword
        arguments if another projection is used.

        %(Axes:kwdoc)s

    Notes
    -----
    .. versionchanged:: 3.8
        In versions prior to 3.8, any preexisting Axes that overlap with the new Axes
        beyond sharing a boundary was deleted. Deletion does not happen in more
        recent versions anymore. Use `.Axes.remove` explicitly if needed.

    If you do not want this behavior, use the `.Figure.add_subplot` method
    or the `.pyplot.axes` function instead.

    If no *kwargs* are passed and there exists an Axes in the location
    specified by *args* then that Axes will be returned rather than a new
    Axes being created.

    If *kwargs* are passed and there exists an Axes in the location
    specified by *args*, the projection type is the same, and the
    *kwargs* match with the existing Axes, then the existing Axes is
    returned.  Otherwise a new Axes is created with the specified
    parameters.  We save a reference to the *kwargs* which we use
    for this comparison.  If any of the values in *kwargs* are
    mutable we will not detect the case where they are mutated.
    In these cases we suggest using `.Figure.add_subplot` and the
    explicit Axes API rather than the implicit pyplot API.

    See Also
    --------
    .Figure.add_subplot
    .pyplot.subplots
    .pyplot.axes
    .Figure.subplots

    Examples
    --------
    ::

        plt.subplot(221)

        # equivalent but more general
        ax1 = plt.subplot(2, 2, 1)

        # add a subplot with no frame
        ax2 = plt.subplot(222, frameon=False)

        # add a polar subplot
        plt.subplot(223, projection='polar')

        # add a red subplot that shares the x-axis with ax1
        plt.subplot(224, sharex=ax1, facecolor='red')

        # delete ax2 from the figure
        plt.delaxes(ax2)

        # add ax2 to the figure again
        plt.subplot(ax2)

        # make the first Axes "current" again
        plt.subplot(221)

    """
    # Here we will only normalize `polar=True` vs `projection='polar'` and let
    # downstream code deal with the rest.
    unset = object()
    projection = kwargs.get('projection', unset)
    polar = kwargs.pop('polar', unset)
    if polar is not unset and polar:
        # if we got mixed messages from the user, raise
        if projection is not unset and projection != 'polar':
            raise ValueError(
                f"polar={polar}, yet projection={projection!r}. "
                "Only one of these arguments should be supplied."
            )
        kwargs['projection'] = projection = 'polar'

    # if subplot called without arguments, create subplot(1, 1, 1)
    if len(args) == 0:
        args = (1, 1, 1)

    # This check was added because it is very easy to type subplot(1, 2, False)
    # when subplots(1, 2, False) was intended (sharex=False, that is). In most
    # cases, no error will ever occur, but mysterious behavior can result
    # because what was intended to be the sharex argument is instead treated as
    # a subplot index for subplot()
    if len(args) >= 3 and isinstance(args[2], bool):
        _api.warn_external("The subplot index argument to subplot() appears "
                           "to be a boolean. Did you intend to use "
                           "subplots()?")
    # Check for nrows and ncols, which are not valid subplot args:
    if 'nrows' in kwargs or 'ncols' in kwargs:
        raise TypeError("subplot() got an unexpected keyword argument 'ncols' "
                        "and/or 'nrows'.  Did you intend to call subplots()?")

    fig = gcf()

    # First, search for an existing subplot with a matching spec.
    key = SubplotSpec._from_subplot_args(fig, args)

    for ax in fig.axes:
        # If we found an Axes at the position, we can reuse it if the user passed no
        # kwargs or if the Axes class and kwargs are identical.
        if (ax.get_subplotspec() == key
            and (kwargs == {}
                 or (ax._projection_init
                     == fig._process_projection_requirements(**kwargs)))):
            break
    else:
        # we have exhausted the known Axes and none match, make a new one!
        ax = fig.add_subplot(*args, **kwargs)

    fig.sca(ax)

    return ax


def subplot(rows, cols, pos, *args, **kwargs):
  ax = plt.subplot(rows, cols, pos, *args, **kwargs)
  ax.tick_params(top=False, right=False)  # Don't interfere with the titles.
  return ax

