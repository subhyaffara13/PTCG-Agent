
def test_series_labels():
    # verify that series return the correct label, depending on the plot
    # type and input arguments. If the user set custom label on a data series,
    # it should returned un-modified.
    if not np:
        skip("numpy not installed.")

    x, y, z, u, v = symbols("x, y, z, u, v")
    wrapper = "$%s$"

    expr = cos(x)
    s1 = LineOver1DRangeSeries(expr, (x, -2, 2), None)
    s2 = LineOver1DRangeSeries(expr, (x, -2, 2), "test")
    assert s1.get_label(False) == str(expr)
    assert s1.get_label(True) == wrapper % latex(expr)
    assert s2.get_label(False) == "test"
    assert s2.get_label(True) == "test"

    s1 = List2DSeries([0, 1, 2, 3], [0, 1, 2, 3], "test")
    assert s1.get_label(False) == "test"
    assert s1.get_label(True) == "test"

    expr = (cos(x), sin(x))
    s1 = Parametric2DLineSeries(*expr, (x, -2, 2), None, use_cm=True)
    s2 = Parametric2DLineSeries(*expr, (x, -2, 2), "test", use_cm=True)
    s3 = Parametric2DLineSeries(*expr, (x, -2, 2), None, use_cm=False)
    s4 = Parametric2DLineSeries(*expr, (x, -2, 2), "test", use_cm=False)
    assert s1.get_label(False) == "x"
    assert s1.get_label(True) == wrapper % "x"
    assert s2.get_label(False) == "test"
    assert s2.get_label(True) == "test"
    assert s3.get_label(False) == str(expr)
    assert s3.get_label(True) == wrapper % latex(expr)
    assert s4.get_label(False) == "test"
    assert s4.get_label(True) == "test"

    expr = (cos(x), sin(x), x)
    s1 = Parametric3DLineSeries(*expr, (x, -2, 2), None, use_cm=True)
    s2 = Parametric3DLineSeries(*expr, (x, -2, 2), "test", use_cm=True)
    s3 = Parametric3DLineSeries(*expr, (x, -2, 2), None, use_cm=False)
    s4 = Parametric3DLineSeries(*expr, (x, -2, 2), "test", use_cm=False)
    assert s1.get_label(False) == "x"
    assert s1.get_label(True) == wrapper % "x"
    assert s2.get_label(False) == "test"
    assert s2.get_label(True) == "test"
    assert s3.get_label(False) == str(expr)
    assert s3.get_label(True) == wrapper % latex(expr)
    assert s4.get_label(False) == "test"
    assert s4.get_label(True) == "test"

    expr = cos(x**2 + y**2)
    s1 = SurfaceOver2DRangeSeries(expr, (x, -2, 2), (y, -2, 2), None)
    s2 = SurfaceOver2DRangeSeries(expr, (x, -2, 2), (y, -2, 2), "test")
    assert s1.get_label(False) == str(expr)
    assert s1.get_label(True) == wrapper % latex(expr)
    assert s2.get_label(False) == "test"
    assert s2.get_label(True) == "test"

    expr = (cos(x - y), sin(x + y), x - y)
    s1 = ParametricSurfaceSeries(*expr, (x, -2, 2), (y, -2, 2), None)
    s2 = ParametricSurfaceSeries(*expr, (x, -2, 2), (y, -2, 2), "test")
    assert s1.get_label(False) == str(expr)
    assert s1.get_label(True) == wrapper % latex(expr)
    assert s2.get_label(False) == "test"
    assert s2.get_label(True) == "test"

    expr = Eq(cos(x - y), 0)
    s1 = ImplicitSeries(expr, (x, -10, 10), (y, -10, 10), None)
    s2 = ImplicitSeries(expr, (x, -10, 10), (y, -10, 10), "test")
    assert s1.get_label(False) == str(expr)
    assert s1.get_label(True) == wrapper % latex(expr)
    assert s2.get_label(False) == "test"
    assert s2.get_label(True) == "test"

