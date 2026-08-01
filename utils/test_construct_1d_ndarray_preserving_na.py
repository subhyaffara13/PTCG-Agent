
def test_construct_1d_ndarray_preserving_na(
    values, dtype, expected, using_infer_string
):
    result = sanitize_array(values, index=None, dtype=dtype)
    if using_infer_string and expected.dtype == object and dtype is None:
        tm.assert_extension_array_equal(result, pd.array(expected, dtype="str"))
    else:
        tm.assert_numpy_array_equal(result, expected)

