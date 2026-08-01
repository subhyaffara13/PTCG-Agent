
def test_dt64arr_addsub_object_dtype_2d(performance_warning):
    # block-wise DataFrame operations will require operating on 2D
    #  DatetimeArray/TimedeltaArray, so check that specifically.
    dti = date_range("1994-02-13", freq="2W", periods=4)
    dta = dti._data.reshape((4, 1))

    other = np.array([[pd.offsets.Day(n)] for n in range(4)])
    assert other.shape == dta.shape

    with tm.assert_produces_warning(performance_warning):
        result = dta + other
    with tm.assert_produces_warning(performance_warning):
        expected = (dta[:, 0] + other[:, 0]).reshape(-1, 1)

    tm.assert_numpy_array_equal(result, expected)

    with tm.assert_produces_warning(performance_warning):
        # Case where we expect to get a TimedeltaArray back
        result2 = dta - dta.astype(object)

    assert result2.shape == (4, 1)
    assert all(td._value == 0 for td in result2.ravel())

