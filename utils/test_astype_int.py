
def test_astype_int(dtype):
    # We choose to ignore the sign and size of integers for
    # Period/Datetime/Timedelta astype
    arr = period_array(["2000", "2001", None], freq="D")

    if np.dtype(dtype) != np.int64:
        with pytest.raises(TypeError, match=r"Do obj.astype\('int64'\)"):
            arr.astype(dtype)
        return

    result = arr.astype(dtype)
    expected = arr._ndarray.view("i8")
    tm.assert_numpy_array_equal(result, expected)


def test_astype_int(dtype):
    arr = pd.array(["1", "2", "3"], dtype=dtype)
    result = arr.astype("int64")
    expected = np.array([1, 2, 3], dtype="int64")
    tm.assert_numpy_array_equal(result, expected)

    arr = pd.array(["1", pd.NA, "3"], dtype=dtype)
    if dtype.na_value is np.nan:
        err = ValueError
        msg = "cannot convert float NaN to integer"
    else:
        err = TypeError
        msg = (
            r"int\(\) argument must be a string, a bytes-like "
            r"object or a( real)? number"
        )
    with pytest.raises(err, match=msg):
        arr.astype("int64")

