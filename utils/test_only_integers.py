
def test_only_integers():
    if not np:
        skip("numpy not installed.")

    x, y, u, v = symbols("x, y, u, v")

    s = LineOver1DRangeSeries(sin(x), (x, -5.5, 4.5), "",
        adaptive=False, only_integers=True)
    xx, _ = s.get_data()
    assert len(xx) == 10
    assert xx[0] == -5 and xx[-1] == 4

    s = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 2 * pi), "",
        adaptive=False, only_integers=True)
    _, _, p = s.get_data()
    assert len(p) == 7
    assert p[0] == 0 and p[-1] == 6

    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, 0, 2 * pi), "",
        adaptive=False, only_integers=True)
    _, _, _, p = s.get_data()
    assert len(p) == 7
    assert p[0] == 0 and p[-1] == 6

    s = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -5.5, 5.5),
        (y, -3.5, 3.5), "",
        adaptive=False, only_integers=True)
    xx, yy, _ = s.get_data()
    assert xx.shape == yy.shape == (7, 11)
    assert np.allclose(xx[:, 0] - (-5) * np.ones(7), 0)
    assert np.allclose(xx[0, :] - np.linspace(-5, 5, 11), 0)
    assert np.allclose(yy[:, 0] - np.linspace(-3, 3, 7), 0)
    assert np.allclose(yy[0, :] - (-3) * np.ones(11), 0)

    r = 2 + sin(7 * u + 5 * v)
    expr = (
        r * cos(u) * sin(v),
        r * sin(u) * sin(v),
        r * cos(v)
    )
    s = ParametricSurfaceSeries(*expr, (u, 0, 2 * pi), (v, 0, pi), "",
        adaptive=False, only_integers=True)
    xx, yy, zz, uu, vv = s.get_data()
    assert xx.shape == yy.shape == zz.shape == uu.shape == vv.shape == (4, 7)

    # only_integers also works with scalar expressions
    s = LineOver1DRangeSeries(1, (x, -5.5, 4.5), "",
        adaptive=False, only_integers=True)
    xx, _ = s.get_data()
    assert len(xx) == 10
    assert xx[0] == -5 and xx[-1] == 4

    s = Parametric2DLineSeries(cos(x), 1, (x, 0, 2 * pi), "",
        adaptive=False, only_integers=True)
    _, _, p = s.get_data()
    assert len(p) == 7
    assert p[0] == 0 and p[-1] == 6

    s = SurfaceOver2DRangeSeries(1, (x, -5.5, 5.5), (y, -3.5, 3.5), "",
        adaptive=False, only_integers=True)
    xx, yy, _ = s.get_data()
    assert xx.shape == yy.shape == (7, 11)
    assert np.allclose(xx[:, 0] - (-5) * np.ones(7), 0)
    assert np.allclose(xx[0, :] - np.linspace(-5, 5, 11), 0)
    assert np.allclose(yy[:, 0] - np.linspace(-3, 3, 7), 0)
    assert np.allclose(yy[0, :] - (-3) * np.ones(11), 0)

    r = 2 + sin(7 * u + 5 * v)
    expr = (
        r * cos(u) * sin(v),
        1,
        r * cos(v)
    )
    s = ParametricSurfaceSeries(*expr, (u, 0, 2 * pi), (v, 0, pi), "",
        adaptive=False, only_integers=True)
    xx, yy, zz, uu, vv = s.get_data()
    assert xx.shape == yy.shape == zz.shape == uu.shape == vv.shape == (4, 7)

