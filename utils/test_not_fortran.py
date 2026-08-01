
def test_not_fortran():
    x = symbols('x')
    g = Function('g')
    with raises(NotImplementedError):
        fcode(gamma(x))
    assert fcode(Integral(sin(x)), strict=False) == "C     Not supported in Fortran:\nC     Integral\n      Integral(sin(x), x)"
    with raises(NotImplementedError):
        fcode(g(x))

