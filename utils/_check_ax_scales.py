
def _check_ax_scales(axes, xaxis="linear", yaxis="linear"):
    """
    Check each axes has expected scales

    Parameters
    ----------
    axes : matplotlib Axes object, or its list-like
    xaxis : {'linear', 'log'}
        expected xaxis scale
    yaxis : {'linear', 'log'}
        expected yaxis scale
    """
    axes = _flatten_visible(axes)
    for ax in axes:
        assert ax.xaxis.get_scale() == xaxis
        assert ax.yaxis.get_scale() == yaxis

