
def test_rendering_kw():
    # verify that each series exposes the `rendering_kw` attribute
    if not np:
        skip("numpy not installed.")

    u, v, x, y, z = symbols("u, v, x:z")

    s = List2DSeries([1, 2, 3], [4, 5, 6])
    assert isinstance(s.rendering_kw, dict)

    s = LineOver1DRangeSeries(1, (x, -5, 5))
    assert isinstance(s.rendering_kw, dict)

    s = Parametric2DLineSeries(sin(x), cos(x), (x, 0, pi))
    assert isinstance(s.rendering_kw, dict)

    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, 0, 2 * pi))
    assert isinstance(s.rendering_kw, dict)

    s = SurfaceOver2DRangeSeries(x + y, (x, -2, 2), (y, -3, 3))
    assert isinstance(s.rendering_kw, dict)

    s = ContourSeries(x + y, (x, -2, 2), (y, -3, 3))
    assert isinstance(s.rendering_kw, dict)

    s = ParametricSurfaceSeries(1, x, y, (x, 0, 1), (y, 0, 1))
    assert isinstance(s.rendering_kw, dict)

