
def test_dataframe_dtypes(method, expected_data, dtypes, min_periods, step):
    df = DataFrame(np.arange(10).reshape((5, 2)), dtype=get_dtype(dtypes))
    rolled = df.rolling(2, min_periods=min_periods, step=step)

    if dtypes in ("m8[ns]", "M8[ns]", "datetime64[ns, UTC]") and method != "count":
        msg = "Cannot aggregate non-numeric type"
        with pytest.raises(DataError, match=msg):
            getattr(rolled, method)()
    else:
        result = getattr(rolled, method)()
        expected = DataFrame(expected_data, dtype="float64")[::step]
        tm.assert_frame_equal(result, expected)

