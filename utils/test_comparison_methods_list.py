
def test_comparison_methods_list(comparison_op, any_string_dtype, box, request):
    dtype = any_string_dtype

    if box is pd.array and dtype != object and dtype.na_value is np.nan:
        mark = pytest.mark.xfail(
            reason="After wrapping list, op returns NotImplemented, see GH#62522"
        )
        request.applymarker(mark)

    op_name = f"__{comparison_op.__name__}__"

    a = box(pd.array(["a", None, "c"], dtype=dtype))
    item = "c"
    other = [None, None, "c"]
    result = comparison_op(a, other)

    # ensure operation is commutative
    result2 = comparison_op(other, a)
    tm.assert_equal(result, result2)

    if dtype == np.dtype(object) or dtype.na_value is np.nan:
        if operator.ne == comparison_op:
            expected = np.array([True, True, False])
        else:
            expected = np.array([False, False, False])
            expected[-1] = getattr(item, op_name)(item)
        if box is not pd.Index:
            # if GH#62766 is addressed this check can be removed
            expected = box(expected, dtype=expected.dtype)
        tm.assert_equal(result, expected)

    else:
        expected_dtype = "boolean[pyarrow]" if dtype.storage == "pyarrow" else "boolean"
        expected = np.full(len(a), fill_value=None, dtype="object")
        expected[-1] = getattr(item, op_name)(item)
        expected = pd.array(expected, dtype=expected_dtype)
        expected = extract_array(expected, extract_numpy=True)
        if box is not pd.Index:
            # if GH#62766 is addressed this check can be removed
            expected = tm.box_expected(expected, box)
        tm.assert_equal(result, expected)

