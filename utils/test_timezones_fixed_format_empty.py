
def test_timezones_fixed_format_empty(temp_hdfstore, tz_aware_fixture, frame_or_series):
    # GH 20594

    dtype = pd.DatetimeTZDtype(tz=tz_aware_fixture)

    obj = Series(dtype=dtype, name="A")
    if frame_or_series is DataFrame:
        obj = obj.to_frame()

    temp_hdfstore["obj"] = obj
    result = temp_hdfstore["obj"]
    tm.assert_equal(result, obj)

