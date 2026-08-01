
def test_to_array_integer():
    result = pd.array([1, 2], dtype="Float64")
    expected = pd.array([1.0, 2.0], dtype="Float64")
    tm.assert_extension_array_equal(result, expected)

    # for integer dtypes, the itemsize is not preserved
    # TODO can we specify "floating" in general?
    result = pd.array(np.array([1, 2], dtype="int32"), dtype="Float64")
    assert result.dtype == Float64Dtype()

