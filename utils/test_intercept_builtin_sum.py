
def test_intercept_builtin_sum():
    s = Series([1.0, 2.0, np.nan, 3.0])
    grouped = s.groupby([0, 1, 2, 2])

    # GH#53425
    result = grouped.agg(builtins.sum)
    # GH#53425
    result2 = grouped.apply(builtins.sum)
    expected = Series([1.0, 2.0, np.nan], index=np.array([0, 1, 2]))
    tm.assert_series_equal(result, expected)
    tm.assert_series_equal(result2, expected)

