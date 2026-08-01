
def test_reindex_downcasting():
    # GH4618 shifted series downcasting
    s = Series(False, index=range(5))
    result = s.shift(1).bfill()
    expected = Series(False, index=range(5), dtype=object)
    tm.assert_series_equal(result, expected)

