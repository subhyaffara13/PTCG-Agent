
def test_series_from_float(data, using_nan_is_na):
    # construct from our dtype & string dtype
    dtype = data.dtype

    # from float
    expected = pd.Series(data)
    np_res = data.to_numpy(na_value=np.nan, dtype="float")
    if not using_nan_is_na:
        np_res = np_res.astype(object)
        np_res[data.isna()] = pd.NA
    result = pd.Series(np_res, dtype=str(dtype))
    tm.assert_series_equal(result, expected)

    # from list
    expected = pd.Series(data)
    result = pd.Series(np.array(data).tolist(), dtype=str(dtype))
    tm.assert_series_equal(result, expected)

