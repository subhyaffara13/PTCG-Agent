
def test_infer_dtype_from_scalar(value, expected, using_infer_string):
    dtype, _ = infer_dtype_from_scalar(value)
    if using_infer_string and value == "foo":
        expected = "string"
    assert is_dtype_equal(dtype, expected)

    with pytest.raises(TypeError, match="must be list-like"):
        infer_dtype_from_array(value)

