
def test_to_numpy_na_value_numpy_dtype(
    index_or_series, values, dtype, na_value, expected
):
    obj = index_or_series(values)
    result = obj.to_numpy(dtype=dtype, na_value=na_value)
    expected = np.array(expected)
    tm.assert_numpy_array_equal(result, expected)

