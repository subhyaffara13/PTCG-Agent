
def test_put_datetime_ser(temp_hdfstore, performance_warning, using_infer_string):
    # https://github.com/pandas-dev/pandas/pull/60663
    ser = Series(3 * [Timestamp("20010102").as_unit("ns")])
    temp_hdfstore.put("ser", ser)
    expected = ser.copy()
    result = temp_hdfstore.get("ser")
    tm.assert_series_equal(result, expected)

