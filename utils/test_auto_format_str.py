
def test_auto_format_str(fmt, value, result):
    """Apply *value* to the format string *fmt*."""
    assert cbook._auto_format_str(fmt, value) == result
    assert cbook._auto_format_str(fmt, np.float64(value)) == result

