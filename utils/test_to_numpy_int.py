
def test_to_numpy_int(box):
    con = pd.Series if box else pd.array

    # no missing values -> can convert to int, otherwise raises
    arr = con([1.0, 2.0, 3.0], dtype="Float64")
    result = arr.to_numpy(dtype="int64")
    expected = np.array([1, 2, 3], dtype="int64")
    tm.assert_numpy_array_equal(result, expected)

    arr = con([1.0, 2.0, None], dtype="Float64")
    with pytest.raises(ValueError, match="cannot convert to 'int64'-dtype"):
        result = arr.to_numpy(dtype="int64")

    # automatic casting (floors the values)
    arr = con([0.1, 0.9, 1.1], dtype="Float64")
    result = arr.to_numpy(dtype="int64")
    expected = np.array([0, 0, 1], dtype="int64")
    tm.assert_numpy_array_equal(result, expected)

