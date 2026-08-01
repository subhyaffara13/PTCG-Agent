
def test_format_decimal(formatter, thousands, precision, func, col):
    styler = DataFrame([[1000000.123456789]], index=[1000000.123456789]).style
    result = getattr(styler, func)(  # testing float
        decimal="_", formatter=formatter, thousands=thousands, precision=precision
    )._translate(True, True)
    assert "000_123" in result["body"][0][col]["display_value"]

    styler = DataFrame([[1 + 1000000.123456789j]], index=[1 + 1000000.123456789j]).style
    result = getattr(styler, func)(  # testing complex
        decimal="_", formatter=formatter, thousands=thousands, precision=precision
    )._translate(True, True)
    assert "000_123" in result["body"][0][col]["display_value"]

