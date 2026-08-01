
def test_is_string_dtype(dtype, expected):
    # GH#54661

    result = com.is_string_dtype(dtype)
    assert result is expected

