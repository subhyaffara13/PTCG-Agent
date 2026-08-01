
def test_bold_headers_arg(styler):
    result = styler.to_html(bold_headers=True)
    assert "th {\n  font-weight: bold;\n}" in result
    result = styler.to_html()
    assert "th {\n  font-weight: bold;\n}" not in result

