
def test_line_color():
    x, y = symbols('x, y')
    p = plot_implicit(x**2 + y**2 - 1, line_color="green", show=False)
    assert p._series[0].line_color == "green"
    p = plot_implicit(x**2 + y**2 - 1, line_color='r', show=False)
    assert p._series[0].line_color == "r"

