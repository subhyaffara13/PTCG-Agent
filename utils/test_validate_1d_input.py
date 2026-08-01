
def test_validate_1d_input(dtype):
    # GH#27125 check that we do not have >1-dimensional input
    msg = "Index data must be 1-dimensional"

    arr = np.arange(8).reshape(2, 2, 2)
    with pytest.raises(ValueError, match=msg):
        Index(arr, dtype=dtype)

    df = DataFrame(arr.reshape(4, 2))
    with pytest.raises(ValueError, match=msg):
        Index(df, dtype=dtype)

    # GH#13601 trying to assign a multi-dimensional array to an index is not allowed
    ser = Series(0, range(4))
    with pytest.raises(ValueError, match=msg):
        ser.index = np.array([[2, 3]] * 4, dtype=dtype)

