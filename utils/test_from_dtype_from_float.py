
def test_from_dtype_from_float(data, using_nan_is_na):
    # construct from our dtype & string dtype
    dtype = data.dtype

    # from float
    expected = pd.Series(data)
    arr = data.to_numpy(na_value=np.nan, dtype="float")
    if using_nan_is_na:
        result = pd.Series(arr, dtype=str(dtype))
        tm.assert_series_equal(result, expected)
    else:
        msg = "Cannot cast NaN value to Integer dtype"
        with pytest.raises(ValueError, match=msg):
            pd.Series(arr, dtype=str(dtype))

    # from int / list
    expected = pd.Series(data)
    result = pd.Series(np.array(data).tolist(), dtype=str(dtype))
    tm.assert_series_equal(result, expected)

    # from int / array
    expected = pd.Series(data).dropna().reset_index(drop=True)
    dropped = np.array(data.dropna()).astype(np.dtype(dtype.type))
    result = pd.Series(dropped, dtype=str(dtype))
    tm.assert_series_equal(result, expected)

