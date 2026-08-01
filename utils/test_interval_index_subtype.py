
def test_interval_index_subtype(timezone, inclusive_endpoints_fixture):
    # GH#46999
    dates = date_range("2022", periods=3, tz=timezone, unit="ns")
    dtype = f"interval[datetime64[ns, {timezone}], {inclusive_endpoints_fixture}]"
    result = IntervalIndex.from_arrays(
        ["2022-01-01", "2022-01-02"],
        ["2022-01-02", "2022-01-03"],
        closed=inclusive_endpoints_fixture,
        dtype=dtype,
    )
    expected = IntervalIndex.from_arrays(
        dates[:-1], dates[1:], closed=inclusive_endpoints_fixture
    )
    tm.assert_index_equal(result, expected)

