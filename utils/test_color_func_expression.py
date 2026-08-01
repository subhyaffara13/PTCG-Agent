
def test_color_func_expression():
    # verify that color_func is able to deal with instances of Expr: they will
    # be lambdified with the same signature used for the main expression.
    if not np:
        skip("numpy not installed.")

    x, y = symbols("x, y")

    s1 = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 2*pi),
        color_func=sin(x), adaptive=False, n=10, use_cm=True)
    s2 = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 2*pi),
        color_func=lambda x: np.cos(x), adaptive=False, n=10, use_cm=True)
    # the following statement should not raise errors
    d1 = s1.get_data()
    assert callable(s1.color_func)
    d2 = s2.get_data()
    assert not np.allclose(d1[-1], d2[-1])

    s = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -pi, pi), (y, -pi, pi),
        color_func=sin(x**2 + y**2), adaptive=False, n1=5, n2=5)
    # the following statement should not raise errors
    s.get_data()
    assert callable(s.color_func)

    xx = [1, 2, 3, 4, 5]
    yy = [1, 2, 3, 4, 5]
    raises(TypeError,
        lambda : List2DSeries(xx, yy, use_cm=True, color_func=sin(x)))

