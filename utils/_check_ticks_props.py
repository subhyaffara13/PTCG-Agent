
def _check_ticks_props(axes, xlabelsize=None, xrot=None, ylabelsize=None, yrot=None):
    """
    Check each axes has expected tick properties

    Parameters
    ----------
    axes : matplotlib Axes object, or its list-like
    xlabelsize : number
        expected xticks font size
    xrot : number
        expected xticks rotation
    ylabelsize : number
        expected yticks font size
    yrot : number
        expected yticks rotation
    """
    from matplotlib.ticker import NullFormatter

    axes = _flatten_visible(axes)
    for ax in axes:
        if xlabelsize is not None or xrot is not None:
            if isinstance(ax.xaxis.get_minor_formatter(), NullFormatter):
                # If minor ticks has NullFormatter, rot / fontsize are not
                # retained
                labels = ax.get_xticklabels()
            else:
                labels = ax.get_xticklabels() + ax.get_xticklabels(minor=True)

            for label in labels:
                if xlabelsize is not None:
                    tm.assert_almost_equal(label.get_fontsize(), xlabelsize)
                if xrot is not None:
                    tm.assert_almost_equal(label.get_rotation(), xrot)

        if ylabelsize is not None or yrot is not None:
            if isinstance(ax.yaxis.get_minor_formatter(), NullFormatter):
                labels = ax.get_yticklabels()
            else:
                labels = ax.get_yticklabels() + ax.get_yticklabels(minor=True)

            for label in labels:
                if ylabelsize is not None:
                    tm.assert_almost_equal(label.get_fontsize(), ylabelsize)
                if yrot is not None:
                    tm.assert_almost_equal(label.get_rotation(), yrot)

