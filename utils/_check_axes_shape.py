
def _check_axes_shape(axes, axes_num=None, layout=None, figsize=None):
    """
    Check expected number of axes is drawn in expected layout

    Parameters
    ----------
    axes : matplotlib Axes object, or its list-like
    axes_num : number
        expected number of axes. Unnecessary axes should be set to
        invisible.
    layout : tuple
        expected layout, (expected number of rows , columns)
    figsize : tuple
        expected figsize. default is matplotlib default
    """
    from pandas.plotting._matplotlib.tools import flatten_axes

    if figsize is None:
        figsize = (6.4, 4.8)
    visible_axes = _flatten_visible(axes)

    if axes_num is not None:
        assert len(visible_axes) == axes_num
        for ax in visible_axes:
            # check something drawn on visible axes
            assert len(ax.get_children()) > 0

    if layout is not None:
        x_set = set()
        y_set = set()
        for ax in flatten_axes(axes):
            # check axes coordinates to estimate layout
            points = ax.get_position().get_points()
            x_set.add(points[0][0])
            y_set.add(points[0][1])
        result = (len(y_set), len(x_set))
        assert result == layout

    tm.assert_numpy_array_equal(
        visible_axes[0].figure.get_size_inches(),
        np.array(figsize, dtype=np.float64),
    )

