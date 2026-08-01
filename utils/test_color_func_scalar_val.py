
def test_color_func_scalar_val():
    # verify that eval_color_func returns a numpy array even when color_func
    # evaluates to a scalar value
    if not np:
        skip("numpy not installed.")

    x, y = symbols("x, y")

    s = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 2*pi),
        adaptive=False, n=10, color_func=lambda t: 1)
    xx, yy, col = s.get_data()
    assert np.allclose(col, np.ones(xx.shape))

    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, 0, 2*pi),
        adaptive=False, n=10, color_func=lambda t: 1)
    xx, yy, zz, col = s.get_data()
    assert np.allclose(col, np.ones(xx.shape))

    s = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -2, 2), (y, -2, 2),
        adaptive=False, n1=10, n2=10, color_func=lambda x: 1)
    xx, yy, zz = s.get_data()
    assert np.allclose(s.eval_color_func(xx), np.ones(xx.shape))

    s = ParametricSurfaceSeries(1, x, y, (x, 0, 1), (y, 0, 1), adaptive=False,
        n1=10, n2=10, color_func=lambda u: 1)
    xx, yy, zz, uu, vv = s.get_data()
    col = s.eval_color_func(xx, yy, zz, uu, vv)
    assert np.allclose(col, np.ones(xx.shape))

