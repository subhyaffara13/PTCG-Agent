
def test_lin_log_scale():
    # Verify that data series create the correct spacing in the data.
    if not np:
        skip("numpy not installed.")

    x, y, z = symbols("x, y, z")

    s = LineOver1DRangeSeries(x, (x, 1, 10), adaptive=False, n=50,
        xscale="linear")
    xx, _ = s.get_data()
    assert np.isclose(xx[1] - xx[0], xx[-1] - xx[-2])

    s = LineOver1DRangeSeries(x, (x, 1, 10), adaptive=False, n=50,
        xscale="log")
    xx, _ = s.get_data()
    assert not np.isclose(xx[1] - xx[0], xx[-1] - xx[-2])

    s = Parametric2DLineSeries(
        cos(x), sin(x), (x, pi / 2, 1.5 * pi), adaptive=False, n=50,
        xscale="linear")
    _, _, param = s.get_data()
    assert np.isclose(param[1] - param[0], param[-1] - param[-2])

    s = Parametric2DLineSeries(
        cos(x), sin(x), (x, pi / 2, 1.5 * pi), adaptive=False, n=50,
        xscale="log")
    _, _, param = s.get_data()
    assert not np.isclose(param[1] - param[0], param[-1] - param[-2])

    s = Parametric3DLineSeries(
        cos(x), sin(x), x, (x, pi / 2, 1.5 * pi), adaptive=False, n=50,
        xscale="linear")
    _, _, _, param = s.get_data()
    assert np.isclose(param[1] - param[0], param[-1] - param[-2])

    s = Parametric3DLineSeries(
        cos(x), sin(x), x, (x, pi / 2, 1.5 * pi), adaptive=False, n=50,
        xscale="log")
    _, _, _, param = s.get_data()
    assert not np.isclose(param[1] - param[0], param[-1] - param[-2])

    s = SurfaceOver2DRangeSeries(
        cos(x ** 2 + y ** 2), (x, 1, 5), (y, 1, 5), n=10,
        xscale="linear", yscale="linear")
    xx, yy, _ = s.get_data()
    assert np.isclose(xx[0, 1] - xx[0, 0], xx[0, -1] - xx[0, -2])
    assert np.isclose(yy[1, 0] - yy[0, 0], yy[-1, 0] - yy[-2, 0])

    s = SurfaceOver2DRangeSeries(
        cos(x ** 2 + y ** 2), (x, 1, 5), (y, 1, 5), n=10,
        xscale="log", yscale="log")
    xx, yy, _ = s.get_data()
    assert not np.isclose(xx[0, 1] - xx[0, 0], xx[0, -1] - xx[0, -2])
    assert not np.isclose(yy[1, 0] - yy[0, 0], yy[-1, 0] - yy[-2, 0])

    s = ImplicitSeries(
        cos(x ** 2 + y ** 2) > 0, (x, 1, 5), (y, 1, 5),
        n1=10, n2=10, xscale="linear", yscale="linear", adaptive=False)
    xx, yy, _, _ = s.get_data()
    assert np.isclose(xx[0, 1] - xx[0, 0], xx[0, -1] - xx[0, -2])
    assert np.isclose(yy[1, 0] - yy[0, 0], yy[-1, 0] - yy[-2, 0])

    s = ImplicitSeries(
        cos(x ** 2 + y ** 2) > 0, (x, 1, 5), (y, 1, 5),
        n=10, xscale="log", yscale="log", adaptive=False)
    xx, yy, _, _ = s.get_data()
    assert not np.isclose(xx[0, 1] - xx[0, 0], xx[0, -1] - xx[0, -2])
    assert not np.isclose(yy[1, 0] - yy[0, 0], yy[-1, 0] - yy[-2, 0])

