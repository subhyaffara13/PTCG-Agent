
def test_use_cm():
    # verify that the `use_cm` attribute is implemented.
    if not np:
        skip("numpy not installed.")

    u, x, y, z = symbols("u, x:z")

    s = List2DSeries([1, 2, 3, 4], [5, 6, 7, 8], use_cm=True)
    assert s.use_cm
    s = List2DSeries([1, 2, 3, 4], [5, 6, 7, 8], use_cm=False)
    assert not s.use_cm

    s = Parametric2DLineSeries(cos(x), sin(x), (x, -4, 3), use_cm=True)
    assert s.use_cm
    s = Parametric2DLineSeries(cos(x), sin(x), (x, -4, 3), use_cm=False)
    assert not s.use_cm

    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, -4, 3),
        use_cm=True)
    assert s.use_cm
    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, -4, 3),
        use_cm=False)
    assert not s.use_cm

    s = SurfaceOver2DRangeSeries(cos(x * y), (x, -4, 3), (y, -2, 5),
        use_cm=True)
    assert s.use_cm
    s = SurfaceOver2DRangeSeries(cos(x * y), (x, -4, 3), (y, -2, 5),
        use_cm=False)
    assert not s.use_cm

    s = ParametricSurfaceSeries(cos(x * y), sin(x * y), x * y,
        (x, -4, 3), (y, -2, 5), use_cm=True)
    assert s.use_cm
    s = ParametricSurfaceSeries(cos(x * y), sin(x * y), x * y,
        (x, -4, 3), (y, -2, 5), use_cm=False)
    assert not s.use_cm

