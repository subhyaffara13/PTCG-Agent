
def test_unwrap():
    # verify that unwrap works as expected
    if not np:
        skip("numpy not installed.")

    x, y = symbols("x, y")
    expr = 1 / (x**3 + 2*x**2 + x)
    expr = arg(expr.subs(x, I*y*2*pi))
    s1 = LineOver1DRangeSeries(expr, (y, 1e-05, 1e05), xscale="log",
        adaptive=False, n=10, unwrap=False)
    s2 = LineOver1DRangeSeries(expr, (y, 1e-05, 1e05), xscale="log",
        adaptive=False, n=10, unwrap=True)
    s3 = LineOver1DRangeSeries(expr, (y, 1e-05, 1e05), xscale="log",
        adaptive=False, n=10, unwrap={"period": 4})
    x1, y1 = s1.get_data()
    x2, y2 = s2.get_data()
    x3, y3 = s3.get_data()
    assert np.allclose(x1, x2)
    # there must not be nan values in the results of these evaluations
    assert all(not np.isnan(t).any() for t in [y1, y2, y3])
    assert not np.allclose(y1, y2)
    assert not np.allclose(y1, y3)
    assert not np.allclose(y2, y3)

