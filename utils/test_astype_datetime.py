
def test_astype_datetime(dtype):
    arr = period_array(["2000", "2001", None], freq="D")
    # slice off the [ns] so that the regex matches.
    if dtype == "timedelta64[ns]":
        with pytest.raises(TypeError, match=dtype[:-4]):
            arr.astype(dtype)

    else:
        # GH#45038 allow period->dt64 because we allow dt64->period
        result = arr.astype(dtype)
        expected = pd.DatetimeIndex(["2000", "2001", pd.NaT], dtype=dtype)._data
        tm.assert_datetime_array_equal(result, expected)

