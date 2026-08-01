
def test_empty_string_datetime_coerce__unit():
    # GH13044
    # coerce empty string to pd.NaT
    result = to_datetime([1, ""], unit="s", errors="coerce")
    expected = DatetimeIndex(["1970-01-01 00:00:01", "NaT"], dtype="datetime64[s]")
    tm.assert_index_equal(expected, result)

    # verify that no exception is raised even when errors='raise' is set
    result = to_datetime([1, ""], unit="s", errors="raise")
    tm.assert_index_equal(expected, result)

