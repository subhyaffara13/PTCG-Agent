
def test_parse_latex_css_conversion_option():
    css = [("command", "option--latex--wrap")]
    expected = [("command", "option--wrap")]
    result = _parse_latex_css_conversion(css)
    assert result == expected

