
def test_is_polar_2d_parametric():
    # verify that Parametric2DLineSeries isable to apply polar discretization,
    # which is used when polar_plot is executed with polar_axis=True
    if not np:
        skip("numpy not installed.")

    t, u = symbols("t u")

    # NOTE: a sufficiently big n must be provided, or else tests
    # are going to fail
    # No colormap
    f = sin(4 * t)
    s1 = Parametric2DLineSeries(f * cos(t), f * sin(t), (t, 0, 2*pi),
        adaptive=False, n=10, is_polar=False, use_cm=False)
    x1, y1, p1 = s1.get_data()
    s2 = Parametric2DLineSeries(f * cos(t), f * sin(t), (t, 0, 2*pi),
        adaptive=False, n=10, is_polar=True, use_cm=False)
    th, r, p2 = s2.get_data()
    assert (not np.allclose(x1, th)) and (not np.allclose(y1, r))
    assert np.allclose(p1, p2)

    # With colormap
    s3 = Parametric2DLineSeries(f * cos(t), f * sin(t), (t, 0, 2*pi),
        adaptive=False, n=10, is_polar=False, color_func=lambda t: 2*t)
    x3, y3, p3 = s3.get_data()
    s4 = Parametric2DLineSeries(f * cos(t), f * sin(t), (t, 0, 2*pi),
        adaptive=False, n=10, is_polar=True, color_func=lambda t: 2*t)
    th4, r4, p4 = s4.get_data()
    assert np.allclose(p3, p4) and (not np.allclose(p1, p3))
    assert np.allclose(x3, x1) and np.allclose(y3, y1)
    assert np.allclose(th4, th) and np.allclose(r4, r)

