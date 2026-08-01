
def test_store_datetime_fractional_secs(temp_hdfstore, unit):
    dt = datetime.datetime(2012, 1, 2, 3, 4, 5, 123456)
    dti = DatetimeIndex([dt], dtype=f"M8[{unit}]")
    series = Series([0], index=dti)
    temp_hdfstore["a"] = series
    assert temp_hdfstore["a"].index[0] == dt

