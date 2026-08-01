
def test_comparison_methods_scalar_pd_na(comparison_op, any_string_dtype):
    dtype = any_string_dtype
    op_name = f"__{comparison_op.__name__}__"
    a = pd.array(["a", None, "c"], dtype=dtype)
    result = getattr(a, op_name)(NA)

    if dtype == np.dtype(object) or dtype.na_value is np.nan:
        if operator.ne == comparison_op:
            expected = np.array([True, True, True])
        else:
            expected = np.array([False, False, False])
        result = extract_array(result, extract_numpy=True)
        tm.assert_numpy_array_equal(result, expected)
    else:
        expected_dtype = "boolean[pyarrow]" if dtype.storage == "pyarrow" else "boolean"
        expected = pd.array([None, None, None], dtype=expected_dtype)
        tm.assert_extension_array_equal(result, expected)
        tm.assert_extension_array_equal(result, expected)

