
def test_infer_dtype_from_array(arr, expected, using_infer_string):
    dtype, _ = infer_dtype_from_array(arr)
    if (
        using_infer_string
        and isinstance(arr, Series)
        and arr.tolist() == ["a", "b", "c"]
    ):
        expected = "string"
    assert is_dtype_equal(dtype, expected)

