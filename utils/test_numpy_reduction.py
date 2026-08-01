
def test_numpy_reduction(test_series):
    result = test_series.resample("YE", closed="right").prod()
    expected = test_series.groupby(lambda x: x.year).agg(np.prod)
    expected.index = result.index
    tm.assert_series_equal(result, expected)

