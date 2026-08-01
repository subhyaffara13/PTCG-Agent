
def test_comparison_methods_array(comparison_op, any_string_dtype, any_string_dtype2):
    op_name = f"__{comparison_op.__name__}__"
    dtype = any_string_dtype
    dtype2 = any_string_dtype2

    a = pd.array(["a", None, "c"], dtype=dtype)
    other = pd.array([None, None, "c"], dtype=dtype2)
    result = comparison_op(a, other)
    result = extract_array(result, extract_numpy=True)

    # ensure operation is commutative
    result2 = comparison_op(other, a)
    result2 = extract_array(result2, extract_numpy=True)
    tm.assert_equal(result, result2)

    if (dtype == object or dtype.na_value is np.nan) and (
        dtype2 == object or dtype2.na_value is np.nan
    ):
        if operator.ne == comparison_op:
            expected = np.array([True, True, False])
        else:
            expected = np.array([False, False, False])
            expected[-1] = getattr(other[-1], op_name)(a[-1])
        result = extract_array(result, extract_numpy=True)
        tm.assert_numpy_array_equal(result, expected)

    else:
        if dtype == object:
            max_dtype = dtype2
        elif dtype2 == object:
            max_dtype = dtype
        else:
            max_dtype = string_dtype_highest_priority(dtype, dtype2)
        if max_dtype.storage == "python":
            expected_dtype = "boolean"
        else:
            expected_dtype = "bool[pyarrow]"

        expected = np.full(len(a), fill_value=None, dtype="object")
        expected[-1] = getattr(other[-1], op_name)(a[-1])
        expected = pd.array(expected, dtype=expected_dtype)
        tm.assert_equal(result, expected)

