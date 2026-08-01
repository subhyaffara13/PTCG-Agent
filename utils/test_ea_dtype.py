
def test_ea_dtype(dtype):
    # GH#56765
    bins = [(0.0, 0.4), (0.4, 0.6)]
    interval_dtype = IntervalDtype(subtype=dtype, closed="left")
    result = IntervalIndex.from_tuples(bins, closed="left", dtype=interval_dtype)
    assert result.dtype == interval_dtype
    expected = IntervalIndex.from_tuples(bins, closed="left").astype(interval_dtype)
    tm.assert_index_equal(result, expected)

