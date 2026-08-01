
def test_error_after_conversions():
    with pytest.raises(TypeError) as exc_info:
        m.test_error_after_conversions("hello")
    assert str(exc_info.value).startswith(
        "Unable to convert function return value to a Python type!"
    )

