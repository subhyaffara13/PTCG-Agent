
def test_reindex_empty_series_tz_dtype():
    # GH 20869
    result = Series(dtype="datetime64[ns, UTC]").reindex([0, 1])
    expected = Series([NaT] * 2, dtype="datetime64[ns, UTC]")
    tm.assert_equal(result, expected)

