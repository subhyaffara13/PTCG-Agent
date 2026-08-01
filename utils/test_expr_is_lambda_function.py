
def test_expr_is_lambda_function():
    # verify that when a numpy function is provided, the series will be able
    # to evaluate it. Also, label should be empty in order to prevent some
    # backend from crashing.
    if not np:
        skip("numpy not installed.")

    f = lambda x: np.cos(x)
    s1 = LineOver1DRangeSeries(f, ("x", -5, 5), adaptive=True, depth=3)
    s1.get_data()
    s2 = LineOver1DRangeSeries(f, ("x", -5, 5), adaptive=False, n=10)
    s2.get_data()
    assert s1.label == s2.label == ""

    fx = lambda x: np.cos(x)
    fy = lambda x: np.sin(x)
    s1 = Parametric2DLineSeries(fx, fy, ("x", 0, 2*pi),
        adaptive=True, adaptive_goal=0.1)
    s1.get_data()
    s2 = Parametric2DLineSeries(fx, fy, ("x", 0, 2*pi),
        adaptive=False, n=10)
    s2.get_data()
    assert s1.label == s2.label == ""

    fz = lambda x: x
    s1 = Parametric3DLineSeries(fx, fy, fz, ("x", 0, 2*pi),
        adaptive=True, adaptive_goal=0.1)
    s1.get_data()
    s2 = Parametric3DLineSeries(fx, fy, fz, ("x", 0, 2*pi),
        adaptive=False, n=10)
    s2.get_data()
    assert s1.label == s2.label == ""

    f = lambda x, y: np.cos(x**2 + y**2)
    s1 = SurfaceOver2DRangeSeries(f, ("a", -2, 2), ("b", -3, 3),
        adaptive=False, n1=10, n2=10)
    s1.get_data()
    s2 = ContourSeries(f, ("a", -2, 2), ("b", -3, 3),
        adaptive=False, n1=10, n2=10)
    s2.get_data()
    assert s1.label == s2.label == ""

    fx = lambda u, v: np.cos(u + v)
    fy = lambda u, v: np.sin(u - v)
    fz = lambda u, v: u * v
    s1 = ParametricSurfaceSeries(fx, fy, fz, ("u", 0, pi), ("v", 0, 2*pi),
        adaptive=False, n1=10, n2=10)
    s1.get_data()
    assert s1.label == ""

    raises(TypeError, lambda: List2DSeries(lambda t: t, lambda t: t))
    raises(TypeError, lambda : ImplicitSeries(lambda t: np.sin(t),
        ("x", -5, 5), ("y", -6, 6)))

