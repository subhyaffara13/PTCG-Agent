
def test_css_convert_apply_index(styler, axis):
    styler.map_index(lambda x: "font-weight: bold;", axis=axis)
    for label in getattr(styler, axis):
        assert f"\\bfseries {label}" in styler.to_latex(convert_css=True)

