
def test_fcode_Pow():
    x, y = symbols('x,y')
    n = symbols('n', integer=True)

    assert fcode(x**3) == "      x**3"
    assert fcode(x**(y**3)) == "      x**(y**3)"
    assert fcode(1/(sin(x)*3.5)**(x - y**x)/(x**2 + y)) == \
        "      (3.5d0*sin(x))**(-x + y**x)/(x**2 + y)"
    assert fcode(sqrt(x)) == '      sqrt(x)'
    assert fcode(sqrt(n)) == '      sqrt(dble(n))'
    assert fcode(x**0.5) == '      sqrt(x)'
    assert fcode(sqrt(x)) == '      sqrt(x)'
    assert fcode(sqrt(10)) == '      sqrt(10.0d0)'
    assert fcode(x**-1.0) == '      1d0/x'
    assert fcode(x**-2.0, 'y', source_format='free') == 'y = x**(-2.0d0)'  # 2823
    assert fcode(x**Rational(3, 7)) == '      x**(3.0d0/7.0d0)'

