
def test_setitem_nan_in_int64_array(dtype, indexer, using_nan_is_na):
    arr = pd.array([0, 1, 2], dtype=dtype)
    if not using_nan_is_na:
        err = TypeError
        msg = "Invalid value 'nan' for dtype 'Int64'"
        if dtype == "int64[pyarrow]":
            import pyarrow as pa

            err = pa.lib.ArrowInvalid
            msg = "Could not convert nan with type float"
        with pytest.raises(err, match=msg):
            arr[indexer] = np.nan
        assert arr[1] == 1
    else:
        arr[indexer] = np.nan
        assert arr[1] is pd.NA

