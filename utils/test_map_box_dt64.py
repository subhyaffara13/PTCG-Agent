
def test_map_box_dt64(unit):
    vals = [pd.Timestamp("2011-01-01"), pd.Timestamp("2011-01-02")]
    ser = Series(vals).dt.as_unit(unit)
    assert ser.dtype == f"datetime64[{unit}]"
    # boxed value must be Timestamp instance
    res = ser.map(lambda x: f"{type(x).__name__}_{x.day}_{x.tz}")
    exp = Series(["Timestamp_1_None", "Timestamp_2_None"])
    tm.assert_series_equal(res, exp)

