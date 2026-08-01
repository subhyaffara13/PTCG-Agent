
def test_update_dtype_raises(original, dtype, expected_error_msg):
    with pytest.raises(ValueError, match=expected_error_msg):
        original.update_dtype(dtype)

