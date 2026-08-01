
def test_rmod_consistent_large_series():
    # GH 29602
    result = Series([2] * 10001).rmod(-1)
    expected = Series([1] * 10001)

    tm.assert_series_equal(result, expected)

