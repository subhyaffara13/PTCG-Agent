
def test_scatter_color_repr_error():

    def get_next_color():   # pragma: no cover
        return 'blue'  # currently unused
    msg = (
            r"'c' argument must be a color, a sequence of colors"
            r", or a sequence of numbers, not 'red\\n'"
        )
    with pytest.raises(ValueError, match=msg):
        c = 'red\n'
        mpl.axes.Axes._parse_scatter_color_args(
            c, None, kwargs={}, xsize=2, get_next_color_func=get_next_color)

