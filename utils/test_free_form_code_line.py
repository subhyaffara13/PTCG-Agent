
def test_free_form_code_line():
    x, y = symbols('x,y')
    assert fcode(cos(x) + sin(y), source_format='free') == "sin(y) + cos(x)"

