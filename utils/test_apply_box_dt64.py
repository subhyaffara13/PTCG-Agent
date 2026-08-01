
def test_apply_box_dt64():
    # ufunc will not be boxed. Same test cases as the test_map_box
    vals = [pd.Timestamp("2011-01-01"), pd.Timestamp("2011-01-02")]
    ser = Series(vals, dtype="M8[ns]")
    assert ser.dtype == "datetime64[ns]"
    # boxed value must be Timestamp instance
    res = ser.apply(lambda x: f"{type(x).__name__}_{x.day}_{x.tz}", by_row="compat")
    exp = Series(["Timestamp_1_None", "Timestamp_2_None"])
    tm.assert_series_equal(res, exp)

