
def test_add_sequence(any_string_dtype, request, using_infer_string):
    dtype = any_string_dtype
    if (
        dtype != object
        and dtype.storage == "python"
        and dtype.na_value is np.nan
        and HAS_PYARROW
        and using_infer_string
    ):
        mark = pytest.mark.xfail(
            reason="As of GH#62522, the list gets wrapped with sanitize_array, "
            "which casts to a higher-priority StringArray, so we get "
            "NotImplemented."
        )
        request.applymarker(mark)
    if dtype == np.dtype(object) and using_infer_string:
        mark = pytest.mark.xfail(reason="Cannot broadcast list")
        request.applymarker(mark)

    a = pd.array(["a", "b", None, None], dtype=dtype)
    other = ["x", None, "y", None]

    result = a + other
    expected = pd.array(["ax", None, None, None], dtype=dtype)
    tm.assert_extension_array_equal(result, expected)

    result = other + a
    expected = pd.array(["xa", None, None, None], dtype=dtype)
    tm.assert_extension_array_equal(result, expected)

