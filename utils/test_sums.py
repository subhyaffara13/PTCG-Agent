
def test_sums():
    # test that data series are able to deal with sums
    if not np:
        skip("numpy not installed.")

    x, y, u = symbols("x, y, u")

    def do_test(data1, data2):
        assert len(data1) == len(data2)
        for d1, d2 in zip(data1, data2):
            assert np.allclose(d1, d2)

    s = LineOver1DRangeSeries(Sum(1 / x ** y, (x, 1, 1000)), (y, 2, 10),
        adaptive=False, only_integers=True)
    xx, yy = s.get_data()

    s1 = LineOver1DRangeSeries(Sum(1 / x, (x, 1, y)), (y, 2, 10),
        adaptive=False, only_integers=True)
    xx1, yy1 = s1.get_data()

    s2 = LineOver1DRangeSeries(Sum(u / x, (x, 1, y)), (y, 2, 10),
        params={u: 1}, only_integers=True)
    xx2, yy2 = s2.get_data()
    xx1 = xx1.astype(float)
    xx2 = xx2.astype(float)
    do_test([xx1, yy1], [xx2, yy2])

    s = LineOver1DRangeSeries(Sum(1 / x, (x, 1, y)), (y, 2, 10),
        adaptive=True)
    with warns(
        UserWarning,
        match="The evaluation with NumPy/SciPy failed",
        test_stacklevel=False,
    ):
        raises(TypeError, lambda: s.get_data())

