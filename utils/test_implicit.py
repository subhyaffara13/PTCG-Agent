
def test_implicit():
    x, y = symbols('x,y')
    assert fcode(sin(x)) == "      sin(x)"
    assert fcode(atan2(x, y)) == "      atan2(x, y)"
    assert fcode(conjugate(x)) == "      conjg(x)"

