from typing import Any

def subplot_mosaic(
    mosaic: str,
    *,
    sharex: bool = ...,
    sharey: bool = ...,
    width_ratios: ArrayLike | None = ...,
    height_ratios: ArrayLike | None = ...,
    empty_sentinel: str = ...,
    subplot_kw: dict[str, Any] | None = ...,
    gridspec_kw: dict[str, Any] | None = ...,
    per_subplot_kw: dict[str | tuple[str, ...], dict[str, Any]] | None = ...,
    **fig_kw: Any
) -> tuple[Figure, dict[str, matplotlib.axes.Axes]]: ...


def subplot_mosaic(
    mosaic: list[HashableList[_T]],
    *,
    sharex: bool = ...,
    sharey: bool = ...,
    width_ratios: ArrayLike | None = ...,
    height_ratios: ArrayLike | None = ...,
    empty_sentinel: _T = ...,
    subplot_kw: dict[str, Any] | None = ...,
    gridspec_kw: dict[str, Any] | None = ...,
    per_subplot_kw: dict[_T | tuple[_T, ...], dict[str, Any]] | None = ...,
    **fig_kw: Any
) -> tuple[Figure, dict[_T, matplotlib.axes.Axes]]: ...


def subplot_mosaic(
    mosaic: list[HashableList[Hashable]],
    *,
    sharex: bool = ...,
    sharey: bool = ...,
    width_ratios: ArrayLike | None = ...,
    height_ratios: ArrayLike | None = ...,
    empty_sentinel: Any = ...,
    subplot_kw: dict[str, Any] | None = ...,
    gridspec_kw: dict[str, Any] | None = ...,
    per_subplot_kw: dict[Hashable | tuple[Hashable, ...], dict[str, Any]] | None = ...,
    **fig_kw: Any
) -> tuple[Figure, dict[Hashable, matplotlib.axes.Axes]]: ...


def subplot_mosaic(
    mosaic: str | list[HashableList[_T]] | list[HashableList[Hashable]],
    *,
    sharex: bool = False,
    sharey: bool = False,
    width_ratios: ArrayLike | None = None,
    height_ratios: ArrayLike | None = None,
    empty_sentinel: Any = '.',
    subplot_kw: dict[str, Any] | None = None,
    gridspec_kw: dict[str, Any] | None = None,
    per_subplot_kw: dict[str | tuple[str, ...], dict[str, Any]] |
                    dict[_T | tuple[_T, ...], dict[str, Any]] |
                    dict[Hashable | tuple[Hashable, ...], dict[str, Any]] | None = None,
    **fig_kw: Any
) -> tuple[Figure, dict[str, matplotlib.axes.Axes]] | \
     tuple[Figure, dict[_T, matplotlib.axes.Axes]] | \
     tuple[Figure, dict[Hashable, matplotlib.axes.Axes]]:
    """
    Build a layout of Axes based on ASCII art or nested lists.

    This is a helper function to build complex GridSpec layouts visually.

    See :ref:`mosaic`
    for an example and full API documentation

    Parameters
    ----------
    mosaic : list of list of {hashable or nested} or str

        A visual layout of how you want your Axes to be arranged
        labeled as strings.  For example ::

           x = [['A panel', 'A panel', 'edge'],
                ['C panel', '.',       'edge']]

        produces 4 Axes:

        - 'A panel' which is 1 row high and spans the first two columns
        - 'edge' which is 2 rows high and is on the right edge
        - 'C panel' which in 1 row and 1 column wide in the bottom left
        - a blank space 1 row and 1 column wide in the bottom center

        Any of the entries in the layout can be a list of lists
        of the same form to create nested layouts.

        If input is a str, then it must be of the form ::

          '''
          AAE
          C.E
          '''

        where each character is a column and each line is a row.
        This only allows only single character Axes labels and does
        not allow nesting but is very terse.

    sharex, sharey : bool, default: False
        If True, the x-axis (*sharex*) or y-axis (*sharey*) will be shared
        among all subplots.  In that case, tick label visibility and axis units
        behave as for `subplots`.  If False, each subplot's x- or y-axis will
        be independent.

    width_ratios : array-like of length *ncols*, optional
        Defines the relative widths of the columns. Each column gets a
        relative width of ``width_ratios[i] / sum(width_ratios)``.
        If not given, all columns will have the same width.  Convenience
        for ``gridspec_kw={'width_ratios': [...]}``.

    height_ratios : array-like of length *nrows*, optional
        Defines the relative heights of the rows. Each row gets a
        relative height of ``height_ratios[i] / sum(height_ratios)``.
        If not given, all rows will have the same height. Convenience
        for ``gridspec_kw={'height_ratios': [...]}``.

    empty_sentinel : object, optional
        Entry in the layout to mean "leave this space empty".  Defaults
        to ``'.'``. Note, if *layout* is a string, it is processed via
        `inspect.cleandoc` to remove leading white space, which may
        interfere with using white-space as the empty sentinel.

    subplot_kw : dict, optional
        Dictionary with keywords passed to the `.Figure.add_subplot` call
        used to create each subplot.  These values may be overridden by
        values in *per_subplot_kw*.

    per_subplot_kw : dict, optional
        A dictionary mapping the Axes identifiers or tuples of identifiers
        to a dictionary of keyword arguments to be passed to the
        `.Figure.add_subplot` call used to create each subplot.  The values
        in these dictionaries have precedence over the values in
        *subplot_kw*.

        If *mosaic* is a string, and thus all keys are single characters,
        it is possible to use a single string instead of a tuple as keys;
        i.e. ``"AB"`` is equivalent to ``("A", "B")``.

        .. versionadded:: 3.7

    gridspec_kw : dict, optional
        Dictionary with keywords passed to the `.GridSpec` constructor used
        to create the grid the subplots are placed on.

    **fig_kw
        All additional keyword arguments are passed to the
        `.pyplot.figure` call.

    Returns
    -------
    fig : `.Figure`
       The new figure

    dict[label, Axes]
       A dictionary mapping the labels to the Axes objects.  The order of
       the Axes is left-to-right and top-to-bottom of their position in the
       total layout.

    """
    num = fig_kw.get('num')
    _raise_if_figure_exists(fig_kw.get('num'), "subplot_mosaic", fig_kw.get('clear'))

    fig = figure(**fig_kw)
    ax_dict = fig.subplot_mosaic(  # type: ignore[misc]
        mosaic,  # type: ignore[arg-type]
        sharex=sharex, sharey=sharey,
        height_ratios=height_ratios, width_ratios=width_ratios,
        subplot_kw=subplot_kw, gridspec_kw=gridspec_kw,
        empty_sentinel=empty_sentinel,
        per_subplot_kw=per_subplot_kw,  # type: ignore[arg-type]
    )
    return fig, ax_dict

