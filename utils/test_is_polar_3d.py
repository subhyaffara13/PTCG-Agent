
def test_is_polar_3d():
    # verify that SurfaceOver2DRangeSeries is able to apply
    # polar discretization
    if not np:
        skip("numpy not installed.")

    x, y, t = symbols("x, y, t")
    expr = (x**2 - 1)**2
    s1 = SurfaceOver2DRangeSeries(expr, (x, 0, 1.5), (y, 0, 2 * pi),
        n=10, adaptive=False, is_polar=False)
    s2 = SurfaceOver2DRangeSeries(expr, (x, 0, 1.5), (y, 0, 2 * pi),
        n=10, adaptive=False, is_polar=True)
    x1, y1, z1 = s1.get_data()
    x2, y2, z2 = s2.get_data()
    x22, y22 = x1 * np.cos(y1), x1 * np.sin(y1)
    assert np.allclose(x2, x22)
    assert np.allclose(y2, y22)

