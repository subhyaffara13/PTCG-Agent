
def test_setitem_float_nan_is_na(using_nan_is_na):
    # GH#61732
    ser = pd.Series([-1, 0, 1], dtype="int64[pyarrow]")

    if using_nan_is_na:
        ser[1] = np.nan
        assert ser.isna()[1]
    else:
        msg = "Could not convert nan with type float: tried to convert to int64"
        with pytest.raises(pa.lib.ArrowInvalid, match=msg):
            ser[1] = np.nan

    ser = pd.Series([-1, np.nan, 1], dtype="float64[pyarrow]")
    if using_nan_is_na:
        assert ser.isna()[1]
        assert ser[1] is pd.NA

        ser[1] = np.nan
        assert ser[1] is pd.NA

    else:
        assert not ser.isna()[1]
        assert isinstance(ser[1], float)
        assert np.isnan(ser[1])

        ser[2] = np.nan
        assert isinstance(ser[2], float)
        assert np.isnan(ser[2])

