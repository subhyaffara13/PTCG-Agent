
def test_setitem_nan_in_float64_array(dtype, indexer, using_nan_is_na):
    arr = pd.array([0, pd.NA, 1], dtype=dtype)

    arr[indexer] = np.nan
    if not using_nan_is_na:
        assert np.isnan(arr[1])
    else:
        assert arr[1] is pd.NA

