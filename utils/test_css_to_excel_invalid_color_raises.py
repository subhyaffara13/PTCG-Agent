
def test_css_to_excel_invalid_color_raises(input_color):
    """Test that invalid colors raise a ValueError."""
    css = (
        f"border-top-color: {input_color}; "
        f"border-right-color: {input_color}; "
        f"border-bottom-color: {input_color}; "
        f"border-left-color: {input_color}; "
        f"background-color: {input_color}; "
        f"color: {input_color}"
    )

    convert = CSSToExcelConverter()
    with pytest.raises(ValueError, match=f"Unexpected color {input_color}"):
        convert(css)

