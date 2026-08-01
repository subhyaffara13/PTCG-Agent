
def test_update_dtype(original, dtype, expected):
    result = original.update_dtype(dtype)
    assert result == expected

