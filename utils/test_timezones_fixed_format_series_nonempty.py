
def test_timezones_fixed_format_series_nonempty(temp_hdfstore, tz_aware_fixture):
    # GH 20594

    dtype = pd.DatetimeTZDtype(tz=tz_aware_fixture)

    s = Series([0], dtype=dtype)
    temp_hdfstore["s"] = s
    result = temp_hdfstore["s"]
    tm.assert_series_equal(result, s)

