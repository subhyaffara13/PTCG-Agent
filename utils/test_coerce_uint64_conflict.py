
def test_coerce_uint64_conflict(data, exp_data):
    # see gh-17007 and gh-17125
    #
    # Still returns float despite the uint64-nan conflict,
    # which would normally force the casting to object.
    result = to_numeric(Series(data), errors="coerce")
    expected = Series(exp_data, dtype=float)
    tm.assert_series_equal(result, expected)

