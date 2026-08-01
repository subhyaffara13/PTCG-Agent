
def test_parse_latex_cell_styles_basic():  # test nesting
    cell_style = [("itshape", "--rwrap"), ("cellcolor", "[rgb]{0,1,1}--rwrap")]
    expected = "\\itshape{\\cellcolor[rgb]{0,1,1}{text}}"
    assert _parse_latex_cell_styles(cell_style, "text") == expected

