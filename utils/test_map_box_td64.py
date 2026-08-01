
def test_map_box_td64(unit):
    # timedelta
    vals = [pd.Timedelta("1 days"), pd.Timedelta("2 days")]
    ser = Series(vals).dt.as_unit(unit)
    assert ser.dtype == f"timedelta64[{unit}]"
    res = ser.map(lambda x: f"{type(x).__name__}_{x.days}")
    exp = Series(["Timedelta_1", "Timedelta_2"])
    tm.assert_series_equal(res, exp)

