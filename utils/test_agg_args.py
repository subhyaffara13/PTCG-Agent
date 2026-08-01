
def test_agg_args(args, kwargs, increment):
    # GH 43357
    def f(x, a=0, b=0, c=0):
        return x + a + 10 * b + 100 * c

    s = Series([1, 2])
    result = s.agg(f, 0, *args, **kwargs)
    expected = s + increment
    tm.assert_series_equal(result, expected)


def test_agg_args(args, kwargs, increment):
    # GH 43357
    def f(x, a=0, b=0, c=0):
        return x + a + 10 * b + 100 * c

    s = Series([1, 2])
    result = s.transform(f, 0, *args, **kwargs)
    expected = s + increment
    tm.assert_series_equal(result, expected)

