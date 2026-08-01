
def test_apply_box_td64():
    # timedelta
    vals = [pd.Timedelta("1 days"), pd.Timedelta("2 days")]
    ser = Series(vals)
    assert ser.dtype == "timedelta64[us]"
    res = ser.apply(lambda x: f"{type(x).__name__}_{x.days}", by_row="compat")
    exp = Series(["Timedelta_1", "Timedelta_2"])
    tm.assert_series_equal(res, exp)

