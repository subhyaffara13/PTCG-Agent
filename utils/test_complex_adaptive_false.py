import re

def test_complex_adaptive_false():
    # verify that series with adaptive=False is evaluated with discretized
    # ranges of type complex.
    if not np:
        skip("numpy not installed.")

    x, y, u = symbols("x y u")

    def do_test(data1, data2):
        assert len(data1) == len(data2)
        for d1, d2 in zip(data1, data2):
            assert np.allclose(d1, d2)

    expr1 = sqrt(x) * exp(-x**2)
    expr2 = sqrt(u * x) * exp(-x**2)
    s1 = LineOver1DRangeSeries(im(expr1), (x, -5, 5), adaptive=False, n=10)
    s2 = LineOver1DRangeSeries(im(expr2), (x, -5, 5),
        adaptive=False, n=10, params={u: 1})
    data1 = s1.get_data()
    data2 = s2.get_data()

    do_test(data1, data2)
    assert (not np.allclose(data1[1], 0)) and (not np.allclose(data2[1], 0))

    s1 = Parametric2DLineSeries(re(expr1), im(expr1), (x, -pi, pi),
        adaptive=False, n=10)
    s2 = Parametric2DLineSeries(re(expr2), im(expr2), (x, -pi, pi),
        adaptive=False, n=10, params={u: 1})
    data1 = s1.get_data()
    data2 = s2.get_data()
    do_test(data1, data2)
    assert (not np.allclose(data1[1], 0)) and (not np.allclose(data2[1], 0))

    s1 = SurfaceOver2DRangeSeries(im(expr1), (x, -5, 5), (y, -10, 10),
        adaptive=False, n1=30, n2=3)
    s2 = SurfaceOver2DRangeSeries(im(expr2), (x, -5, 5), (y, -10, 10),
        adaptive=False, n1=30, n2=3, params={u: 1})
    data1 = s1.get_data()
    data2 = s2.get_data()
    do_test(data1, data2)
    assert (not np.allclose(data1[1], 0)) and (not np.allclose(data2[1], 0))

