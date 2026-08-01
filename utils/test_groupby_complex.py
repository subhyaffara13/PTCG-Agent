
def test_groupby_complex():
    # GH 12902
    a = Series(data=np.arange(4) * (1 + 2j), index=[0, 0, 1, 1])
    expected = Series((1 + 2j, 5 + 10j), index=Index([0, 1]))

    result = a.groupby(level=0).sum()
    tm.assert_series_equal(result, expected)


def test_groupby_complex(func, output):
    # GH#43701
    data = Series(np.arange(20).reshape(10, 2).dot([1, 2j]))
    result = data.groupby(data.index % 2).agg(func)
    expected = Series(output)
    tm.assert_series_equal(result, expected)

