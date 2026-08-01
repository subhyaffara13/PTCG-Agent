
def test_color_func():
    # verify that eval_color_func produces the expected results in order to
    # maintain back compatibility with the old sympy.plotting module
    if not np:
        skip("numpy not installed.")

    x, y, z, u, v = symbols("x, y, z, u, v")

    # color func: returns x, y, color and s is parametric
    xx = np.linspace(-3, 3, 10)
    yy1 = np.cos(xx)
    s = List2DSeries(xx, yy1, color_func=lambda x, y: 2 * x, use_cm=True)
    xxs, yys, col = s.get_data()
    assert np.allclose(xx, xxs)
    assert np.allclose(yy1, yys)
    assert np.allclose(2 * xx, col)
    assert s.is_parametric

    s = List2DSeries(xx, yy1, color_func=lambda x, y: 2 * x, use_cm=False)
    assert len(s.get_data()) == 2
    assert not s.is_parametric

    s = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 2*pi),
        adaptive=False, n=10, color_func=lambda t: t)
    xx, yy, col = s.get_data()
    assert (not np.allclose(xx, col)) and (not np.allclose(yy, col))
    s = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 2*pi),
        adaptive=False, n=10, color_func=lambda x, y: x * y)
    xx, yy, col = s.get_data()
    assert np.allclose(col, xx * yy)
    s = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 2*pi),
        adaptive=False, n=10, color_func=lambda x, y, t: x * y * t)
    xx, yy, col = s.get_data()
    assert np.allclose(col, xx * yy * np.linspace(0, 2*np.pi, 10))

    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, 0, 2*pi),
        adaptive=False, n=10, color_func=lambda t: t)
    xx, yy, zz, col = s.get_data()
    assert (not np.allclose(xx, col)) and (not np.allclose(yy, col))
    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, 0, 2*pi),
        adaptive=False, n=10, color_func=lambda x, y, z: x * y * z)
    xx, yy, zz, col = s.get_data()
    assert np.allclose(col, xx * yy * zz)
    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, 0, 2*pi),
        adaptive=False, n=10, color_func=lambda x, y, z, t: x * y * z * t)
    xx, yy, zz, col = s.get_data()
    assert np.allclose(col, xx * yy * zz * np.linspace(0, 2*np.pi, 10))

    s = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -2, 2), (y, -2, 2),
        adaptive=False, n1=10, n2=10, color_func=lambda x: x)
    xx, yy, zz = s.get_data()
    col = s.eval_color_func(xx, yy, zz)
    assert np.allclose(xx, col)
    s = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -2, 2), (y, -2, 2),
        adaptive=False, n1=10, n2=10, color_func=lambda x, y: x * y)
    xx, yy, zz = s.get_data()
    col = s.eval_color_func(xx, yy, zz)
    assert np.allclose(xx * yy, col)
    s = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -2, 2), (y, -2, 2),
        adaptive=False, n1=10, n2=10, color_func=lambda x, y, z: x * y * z)
    xx, yy, zz = s.get_data()
    col = s.eval_color_func(xx, yy, zz)
    assert np.allclose(xx * yy * zz, col)

    s = ParametricSurfaceSeries(1, x, y, (x, 0, 1), (y, 0, 1), adaptive=False,
        n1=10, n2=10, color_func=lambda u:u)
    xx, yy, zz, uu, vv = s.get_data()
    col = s.eval_color_func(xx, yy, zz, uu, vv)
    assert np.allclose(uu, col)
    s = ParametricSurfaceSeries(1, x, y, (x, 0, 1), (y, 0, 1), adaptive=False,
        n1=10, n2=10, color_func=lambda u, v: u * v)
    xx, yy, zz, uu, vv = s.get_data()
    col = s.eval_color_func(xx, yy, zz, uu, vv)
    assert np.allclose(uu * vv, col)
    s = ParametricSurfaceSeries(1, x, y, (x, 0, 1), (y, 0, 1), adaptive=False,
        n1=10, n2=10, color_func=lambda x, y, z: x * y * z)
    xx, yy, zz, uu, vv = s.get_data()
    col = s.eval_color_func(xx, yy, zz, uu, vv)
    assert np.allclose(xx * yy * zz, col)
    s = ParametricSurfaceSeries(1, x, y, (x, 0, 1), (y, 0, 1), adaptive=False,
        n1=10, n2=10, color_func=lambda x, y, z, u, v: x * y * z * u * v)
    xx, yy, zz, uu, vv = s.get_data()
    col = s.eval_color_func(xx, yy, zz, uu, vv)
    assert np.allclose(xx * yy * zz * uu * vv, col)

    # Interactive Series
    s = List2DSeries([0, 1, 2, x], [x, 2, 3, 4],
        color_func=lambda x, y: 2 * x, params={x: 1}, use_cm=True)
    xx, yy, col = s.get_data()
    assert np.allclose(xx, [0, 1, 2, 1])
    assert np.allclose(yy, [1, 2, 3, 4])
    assert np.allclose(2 * xx, col)
    assert s.is_parametric and s.use_cm

    s = List2DSeries([0, 1, 2, x], [x, 2, 3, 4],
        color_func=lambda x, y: 2 * x, params={x: 1}, use_cm=False)
    assert len(s.get_data()) == 2
    assert not s.is_parametric

