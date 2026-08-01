
def test_series_dtypes(
    method, data, expected_data, coerce_int, dtypes, min_periods, step
):
    ser = Series(data, dtype=get_dtype(dtypes, coerce_int=coerce_int))
    rolled = ser.rolling(2, min_periods=min_periods, step=step)

    if dtypes in ("m8[ns]", "M8[ns]", "datetime64[ns, UTC]") and method != "count":
        msg = "No numeric types to aggregate"
        with pytest.raises(DataError, match=msg):
            getattr(rolled, method)()
    else:
        result = getattr(rolled, method)()
        expected = Series(expected_data, dtype="float64")[::step]
        tm.assert_almost_equal(result, expected)

