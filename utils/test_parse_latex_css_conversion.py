
def test_parse_latex_css_conversion(css, expected):
    result = _parse_latex_css_conversion(css)
    assert result == expected

