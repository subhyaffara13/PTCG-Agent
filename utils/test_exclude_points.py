
def test_exclude_points():
    # verify that exclude works as expected
    if not np:
        skip("numpy not installed.")

    x = symbols("x")

    expr = (floor(x) + S.Half) / (1 - (x - S.Half)**2)

    with warns(
            UserWarning,
            match="NumPy is unable to evaluate with complex numbers some",
            test_stacklevel=False,
        ):
        s = LineOver1DRangeSeries(expr, (x, -3.5, 3.5), adaptive=False, n=100,
            exclude=list(range(-3, 4)))
        xx, yy = s.get_data()
        assert not np.isnan(xx).any()
        assert np.count_nonzero(np.isnan(yy)) == 7
        assert len(xx) > 100

    e1 = log(floor(x)) * cos(x)
    e2 = log(floor(x)) * sin(x)
    with warns(
            UserWarning,
            match="NumPy is unable to evaluate with complex numbers some",
            test_stacklevel=False,
        ):
        s = Parametric2DLineSeries(e1, e2, (x, 1, 12), adaptive=False, n=100,
            exclude=list(range(1, 13)))
        xx, yy, pp = s.get_data()
        assert not np.isnan(pp).any()
        assert np.count_nonzero(np.isnan(xx)) == 11
        assert np.count_nonzero(np.isnan(yy)) == 11
        assert len(xx) > 100

