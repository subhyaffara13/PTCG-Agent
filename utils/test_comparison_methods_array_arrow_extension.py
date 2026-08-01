
def test_comparison_methods_array_arrow_extension(comparison_op, any_string_dtype):
    # Test pd.ArrowDtype(pa.string()) against other string arrays
    import pyarrow as pa

    dtype2 = any_string_dtype

    op_name = f"__{comparison_op.__name__}__"
    dtype = ArrowDtype(pa.string())
    a = pd.array(["a", None, "c"], dtype=dtype)
    other = pd.array([None, None, "c"], dtype=dtype2)
    result = comparison_op(a, other)

    # ensure operation is commutative
    result2 = comparison_op(other, a)
    tm.assert_equal(result, result2)

    expected = pd.array([None, None, True], dtype="bool[pyarrow]")
    expected[-1] = getattr(other[-1], op_name)(a[-1])
    tm.assert_extension_array_equal(result, expected)

