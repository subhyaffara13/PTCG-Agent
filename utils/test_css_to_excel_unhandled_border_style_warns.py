
def test_css_to_excel_unhandled_border_style_warns(css):
    """Test that unhandled border styles raise a CSSWarning."""
    convert = CSSToExcelConverter()
    with tm.assert_produces_warning(CSSWarning, match="Unhandled border style format"):
        convert(css)

