
def test_css_to_excel(css, expected):
    convert = CSSToExcelConverter()
    assert expected == convert(css)

