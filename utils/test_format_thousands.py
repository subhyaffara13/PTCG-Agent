
def test_format_thousands(formatter, decimal, precision, func, col):
    styler = DataFrame([[1000000.123456789]], index=[1000000.123456789]).style
    result = getattr(styler, func)(  # testing float
        thousands="_", formatter=formatter, decimal=decimal, precision=precision
    )._translate(True, True)
    assert "1_000_000" in result["body"][0][col]["display_value"]

    styler = DataFrame([[1000000]], index=[1000000]).style
    result = getattr(styler, func)(  # testing int
        thousands="_", formatter=formatter, decimal=decimal, precision=precision
    )._translate(True, True)
    assert "1_000_000" in result["body"][0][col]["display_value"]

    styler = DataFrame([[1 + 1000000.123456789j]], index=[1 + 1000000.123456789j]).style
    result = getattr(styler, func)(  # testing complex
        thousands="_", formatter=formatter, decimal=decimal, precision=precision
    )._translate(True, True)
    assert "1_000_000" in result["body"][0][col]["display_value"]

