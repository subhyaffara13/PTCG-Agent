import re

def test_detect_poles():
    if not np:
        skip("numpy not installed.")

    x, u = symbols("x, u")

    s1 = LineOver1DRangeSeries(tan(x), (x, -pi, pi),
        adaptive=False, n=1000, detect_poles=False)
    xx1, yy1 = s1.get_data()
    s2 = LineOver1DRangeSeries(tan(x), (x, -pi, pi),
        adaptive=False, n=1000, detect_poles=True, eps=0.01)
    xx2, yy2 = s2.get_data()
    # eps is too small: doesn't detect any poles
    s3 = LineOver1DRangeSeries(tan(x), (x, -pi, pi),
        adaptive=False, n=1000, detect_poles=True, eps=1e-06)
    xx3, yy3 = s3.get_data()
    s4 = LineOver1DRangeSeries(tan(x), (x, -pi, pi),
        adaptive=False, n=1000, detect_poles="symbolic")
    xx4, yy4 = s4.get_data()

    assert np.allclose(xx1, xx2) and np.allclose(xx1, xx3) and np.allclose(xx1, xx4)
    assert not np.any(np.isnan(yy1))
    assert not np.any(np.isnan(yy3))
    assert np.any(np.isnan(yy2))
    assert np.any(np.isnan(yy4))
    assert len(s2.poles_locations) == len(s3.poles_locations) == 0
    assert len(s4.poles_locations) == 2
    assert np.allclose(np.abs(s4.poles_locations), np.pi / 2)

    with warns(
            UserWarning,
            match="NumPy is unable to evaluate with complex numbers some of",
            test_stacklevel=False,
        ):
        s1 = LineOver1DRangeSeries(frac(x), (x, -10, 10),
            adaptive=False, n=1000, detect_poles=False)
        s2 = LineOver1DRangeSeries(frac(x), (x, -10, 10),
            adaptive=False, n=1000, detect_poles=True, eps=0.05)
        s3 = LineOver1DRangeSeries(frac(x), (x, -10, 10),
            adaptive=False, n=1000, detect_poles="symbolic")
        xx1, yy1 = s1.get_data()
        xx2, yy2 = s2.get_data()
        xx3, yy3 = s3.get_data()
        assert np.allclose(xx1, xx2) and np.allclose(xx1, xx3)
        assert not np.any(np.isnan(yy1))
        assert np.any(np.isnan(yy2)) and np.any(np.isnan(yy2))
        assert not np.allclose(yy1, yy2, equal_nan=True)
        # The poles below are actually step discontinuities.
        assert len(s3.poles_locations) == 21

    s1 = LineOver1DRangeSeries(tan(u * x), (x, -pi, pi), params={u: 1},
        adaptive=False, n=1000, detect_poles=False)
    xx1, yy1 = s1.get_data()
    s2 = LineOver1DRangeSeries(tan(u * x), (x, -pi, pi), params={u: 1},
        adaptive=False, n=1000, detect_poles=True, eps=0.01)
    xx2, yy2 = s2.get_data()
    # eps is too small: doesn't detect any poles
    s3 = LineOver1DRangeSeries(tan(u * x), (x, -pi, pi), params={u: 1},
        adaptive=False, n=1000, detect_poles=True, eps=1e-06)
    xx3, yy3 = s3.get_data()
    s4 = LineOver1DRangeSeries(tan(u * x), (x, -pi, pi), params={u: 1},
        adaptive=False, n=1000, detect_poles="symbolic")
    xx4, yy4 = s4.get_data()

    assert np.allclose(xx1, xx2) and np.allclose(xx1, xx3) and np.allclose(xx1, xx4)
    assert not np.any(np.isnan(yy1))
    assert not np.any(np.isnan(yy3))
    assert np.any(np.isnan(yy2))
    assert np.any(np.isnan(yy4))
    assert len(s2.poles_locations) == len(s3.poles_locations) == 0
    assert len(s4.poles_locations) == 2
    assert np.allclose(np.abs(s4.poles_locations), np.pi / 2)

    with warns(
            UserWarning,
            match="NumPy is unable to evaluate with complex numbers some of",
            test_stacklevel=False,
        ):
        u, v = symbols("u, v", real=True)
        n = S(1) / 3
        f = (u + I * v)**n
        r, i = re(f), im(f)
        s1 = Parametric2DLineSeries(r.subs(u, -2), i.subs(u, -2), (v, -2, 2),
            adaptive=False, n=1000, detect_poles=False)
        s2 = Parametric2DLineSeries(r.subs(u, -2), i.subs(u, -2), (v, -2, 2),
            adaptive=False, n=1000, detect_poles=True)
    with ignore_warnings(RuntimeWarning):
        xx1, yy1, pp1 = s1.get_data()
        assert not np.isnan(yy1).any()
        xx2, yy2, pp2 = s2.get_data()
        assert np.isnan(yy2).any()

    with warns(
            UserWarning,
            match="NumPy is unable to evaluate with complex numbers some of",
            test_stacklevel=False,
        ):
        f = (x * u + x * I * v)**n
        r, i = re(f), im(f)
        s1 = Parametric2DLineSeries(r.subs(u, -2), i.subs(u, -2),
            (v, -2, 2), params={x: 1},
            adaptive=False, n1=1000, detect_poles=False)
        s2 = Parametric2DLineSeries(r.subs(u, -2), i.subs(u, -2),
            (v, -2, 2), params={x: 1},
            adaptive=False, n1=1000, detect_poles=True)
    with ignore_warnings(RuntimeWarning):
        xx1, yy1, pp1 = s1.get_data()
        assert not np.isnan(yy1).any()
        xx2, yy2, pp2 = s2.get_data()
        assert np.isnan(yy2).any()

