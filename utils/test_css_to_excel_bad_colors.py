
def test_css_to_excel_bad_colors(input_color):
    # see gh-18392
    css = (
        f"border-top-color: {input_color}; "
        f"border-right-color: {input_color}; "
        f"border-bottom-color: {input_color}; "
        f"border-left-color: {input_color}; "
        f"background-color: {input_color}; "
        f"color: {input_color}"
    )

    expected = {}

    if input_color is not None:
        expected["fill"] = {"patternType": "solid"}

    with tm.assert_produces_warning(CSSWarning, match="Unhandled color format"):
        convert = CSSToExcelConverter()
        assert expected == convert(css)

