
def test_surface_use_cm():
    # verify that SurfaceOver2DRangeSeries and ParametricSurfaceSeries get
    # the same value for use_cm

    x, y, u, v = symbols("x, y, u, v")

    # they read the same value from default settings
    s1 = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -2, 2), (y, -2, 2))
    s2 = ParametricSurfaceSeries(u * cos(v), u * sin(v), u,
        (u, 0, 1), (v, 0 , 2*pi))
    assert s1.use_cm == s2.use_cm

    # they get the same value
    s1 = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -2, 2), (y, -2, 2),
        use_cm=False)
    s2 = ParametricSurfaceSeries(u * cos(v), u * sin(v), u,
        (u, 0, 1), (v, 0 , 2*pi), use_cm=False)
    assert s1.use_cm == s2.use_cm

    # they get the same value
    s1 = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -2, 2), (y, -2, 2),
        use_cm=True)
    s2 = ParametricSurfaceSeries(u * cos(v), u * sin(v), u,
        (u, 0, 1), (v, 0 , 2*pi), use_cm=True)
    assert s1.use_cm == s2.use_cm

