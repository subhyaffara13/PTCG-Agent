
def test_short_caption(styler):
    result = styler.to_latex(caption=("full cap", "short cap"))
    assert "\\caption[short cap]{full cap}" in result

