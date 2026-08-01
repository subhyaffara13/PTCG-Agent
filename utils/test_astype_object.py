
def test_astype_object(dtype):
    arr = pd.array([1.0, pd.NA], dtype=dtype)

    result = arr.astype(object)
    expected = np.array([1.0, pd.NA], dtype=object)
    tm.assert_numpy_array_equal(result, expected)
    # check exact element types
    assert isinstance(result[0], float)
    assert result[1] is pd.NA

