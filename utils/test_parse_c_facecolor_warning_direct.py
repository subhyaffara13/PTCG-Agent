
def test_parse_c_facecolor_warning_direct(c, facecolor):
    """Test the internal _parse_scatter_color_args method directly."""
    def get_next_color():   # pragma: no cover
        return 'blue'  # currently unused

    # Test with facecolors (plural)
    with pytest.warns(UserWarning, match=WARN_MSG):
        mpl.axes.Axes._parse_scatter_color_args(
            c=c, edgecolors=None, kwargs={'facecolors': facecolor},
            xsize=2, get_next_color_func=get_next_color)

    # Test with facecolor (singular)
    with pytest.warns(UserWarning, match=WARN_MSG):
        mpl.axes.Axes._parse_scatter_color_args(
            c=c, edgecolors=None, kwargs={'facecolor': facecolor},
            xsize=2, get_next_color_func=get_next_color)

