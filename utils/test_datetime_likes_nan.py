
def test_datetime_likes_nan(klass, nat):
    dtype = np.dtype(klass.__name__ + "[ns]")
    arr = np.array([1, 2, np.nan])

    exp = np.array([1, 2, nat], dtype)
    res = maybe_downcast_to_dtype(arr, dtype)
    tm.assert_numpy_array_equal(res, exp)

