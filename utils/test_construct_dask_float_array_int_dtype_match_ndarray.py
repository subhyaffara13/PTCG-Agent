
def test_construct_dask_float_array_int_dtype_match_ndarray():
    # GH#40110 make sure we treat a float-dtype dask array with the same
    #  rules we would for an ndarray
    dd = pytest.importorskip("dask.dataframe")

    arr = np.array([1, 2.5, 3])
    darr = dd.from_array(arr)

    res = Series(darr)
    expected = Series(arr)
    tm.assert_series_equal(res, expected)

    # GH#49599 in 2.0 we raise instead of silently ignoring the dtype
    msg = "Trying to coerce float values to integers"
    with pytest.raises(ValueError, match=msg):
        Series(darr, dtype="i8")

    msg = r"Cannot convert non-finite values \(NA or inf\) to integer"
    arr[2] = np.nan
    with pytest.raises(IntCastingNaNError, match=msg):
        Series(darr, dtype="i8")
    # which is the same as we get with a numpy input
    with pytest.raises(IntCastingNaNError, match=msg):
        Series(arr, dtype="i8")

