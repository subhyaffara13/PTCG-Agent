
def test_parse_scatter_color_args_error():
    def get_next_color():   # pragma: no cover
        return 'blue'  # currently unused

    with pytest.raises(ValueError,
                       match="RGBA values should be within 0-1 range"):
        c = np.array([[0.1, 0.2, 0.7], [0.2, 0.4, 1.4]])  # value > 1
        mpl.axes.Axes._parse_scatter_color_args(
            c, None, kwargs={}, xsize=2, get_next_color_func=get_next_color)

