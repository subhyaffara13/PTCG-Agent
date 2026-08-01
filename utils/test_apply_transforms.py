
def test_apply_transforms():
    # verify that transformation functions get applied to the output
    # of data series
    if not np:
        skip("numpy not installed.")

    x, y, z, u, v = symbols("x:z, u, v")

    s1 = LineOver1DRangeSeries(cos(x), (x, -2*pi, 2*pi), adaptive=False, n=10)
    s2 = LineOver1DRangeSeries(cos(x), (x, -2*pi, 2*pi), adaptive=False, n=10,
        tx=np.rad2deg)
    s3 = LineOver1DRangeSeries(cos(x), (x, -2*pi, 2*pi), adaptive=False, n=10,
        ty=np.rad2deg)
    s4 = LineOver1DRangeSeries(cos(x), (x, -2*pi, 2*pi), adaptive=False, n=10,
        tx=np.rad2deg, ty=np.rad2deg)

    x1, y1 = s1.get_data()
    x2, y2 = s2.get_data()
    x3, y3 = s3.get_data()
    x4, y4 = s4.get_data()
    assert np.isclose(x1[0], -2*np.pi) and np.isclose(x1[-1], 2*np.pi)
    assert (y1.min() < -0.9) and (y1.max() > 0.9)
    assert np.isclose(x2[0], -360) and np.isclose(x2[-1], 360)
    assert (y2.min() < -0.9) and (y2.max() > 0.9)
    assert np.isclose(x3[0], -2*np.pi) and np.isclose(x3[-1], 2*np.pi)
    assert (y3.min() < -52) and (y3.max() > 52)
    assert np.isclose(x4[0], -360) and np.isclose(x4[-1], 360)
    assert (y4.min() < -52) and (y4.max() > 52)

    xx = np.linspace(-2*np.pi, 2*np.pi, 10)
    yy = np.cos(xx)
    s1 = List2DSeries(xx, yy)
    s2 = List2DSeries(xx, yy, tx=np.rad2deg, ty=np.rad2deg)
    x1, y1 = s1.get_data()
    x2, y2 = s2.get_data()
    assert np.isclose(x1[0], -2*np.pi) and np.isclose(x1[-1], 2*np.pi)
    assert (y1.min() < -0.9) and (y1.max() > 0.9)
    assert np.isclose(x2[0], -360) and np.isclose(x2[-1], 360)
    assert (y2.min() < -52) and (y2.max() > 52)

    s1 = Parametric2DLineSeries(
        sin(x), cos(x), (x, -pi, pi), adaptive=False, n=10)
    s2 = Parametric2DLineSeries(
        sin(x), cos(x), (x, -pi, pi), adaptive=False, n=10,
        tx=np.rad2deg, ty=np.rad2deg, tp=np.rad2deg)
    x1, y1, a1 = s1.get_data()
    x2, y2, a2 = s2.get_data()
    assert np.allclose(x1, np.deg2rad(x2))
    assert np.allclose(y1, np.deg2rad(y2))
    assert np.allclose(a1, np.deg2rad(a2))

    s1 =  Parametric3DLineSeries(
        sin(x), cos(x), x, (x, -pi, pi), adaptive=False, n=10)
    s2 = Parametric3DLineSeries(
        sin(x), cos(x), x, (x, -pi, pi), adaptive=False, n=10, tp=np.rad2deg)
    x1, y1, z1, a1 = s1.get_data()
    x2, y2, z2, a2 = s2.get_data()
    assert np.allclose(x1, x2)
    assert np.allclose(y1, y2)
    assert np.allclose(z1, z2)
    assert np.allclose(a1, np.deg2rad(a2))

    s1 = SurfaceOver2DRangeSeries(
        cos(x**2 + y**2), (x, -2*pi, 2*pi), (y, -2*pi, 2*pi),
        adaptive=False, n1=10, n2=10)
    s2 = SurfaceOver2DRangeSeries(
        cos(x**2 + y**2), (x, -2*pi, 2*pi), (y, -2*pi, 2*pi),
        adaptive=False, n1=10, n2=10,
        tx=np.rad2deg, ty=lambda x: 2*x, tz=lambda x: 3*x)
    x1, y1, z1 = s1.get_data()
    x2, y2, z2 = s2.get_data()
    assert np.allclose(x1, np.deg2rad(x2))
    assert np.allclose(y1, y2 / 2)
    assert np.allclose(z1, z2 / 3)

    s1 = ParametricSurfaceSeries(
        u + v, u - v, u * v, (u, 0, 2*pi), (v, 0, pi),
        adaptive=False, n1=10, n2=10)
    s2 = ParametricSurfaceSeries(
        u + v, u - v, u * v, (u, 0, 2*pi), (v, 0, pi),
        adaptive=False, n1=10, n2=10,
        tx=np.rad2deg, ty=lambda x: 2*x, tz=lambda x: 3*x)
    x1, y1, z1, u1, v1 = s1.get_data()
    x2, y2, z2, u2, v2 = s2.get_data()
    assert np.allclose(x1, np.deg2rad(x2))
    assert np.allclose(y1, y2 / 2)
    assert np.allclose(z1, z2 / 3)
    assert np.allclose(u1, u2)
    assert np.allclose(v1, v2)

