
def test_where_array_like(klass):
    # see gh-15414
    s = Series([1, 2, 3])
    cond = [False, True, True]
    expected = Series([np.nan, 2, 3])

    result = s.where(klass(cond))
    tm.assert_series_equal(result, expected)

