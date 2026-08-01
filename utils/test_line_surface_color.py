
def test_line_surface_color():
    # verify the back-compatibility with the old sympy.plotting module.
    # By setting line_color or surface_color to be a callable, it will set
    # the color_func attribute.

    x, y, z = symbols("x, y, z")

    s = LineOver1DRangeSeries(sin(x), (x, -5, 5), adaptive=False, n=10,
        line_color=lambda x: x)
    assert (s.line_color is None) and callable(s.color_func)

    s = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 2*pi),
        adaptive=False, n=10, line_color=lambda t: t)
    assert (s.line_color is None) and callable(s.color_func)

    s = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -2, 2), (y, -2, 2),
        n1=10, n2=10, surface_color=lambda x: x)
    assert (s.surface_color is None) and callable(s.color_func)

