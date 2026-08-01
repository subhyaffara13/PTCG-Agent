
def test_match_real_imag():
    x, y = symbols('x,y', real=True)
    i = Symbol('i', imaginary=True)
    assert match_real_imag(S.One) == (1, 0)
    assert match_real_imag(I) == (0, 1)
    assert match_real_imag(3 - 5*I) == (3, -5)
    assert match_real_imag(-sqrt(3) + S.Half*I) == (-sqrt(3), S.Half)
    assert match_real_imag(x + y*I) == (x, y)
    assert match_real_imag(x*I + y*I) == (0, x + y)
    assert match_real_imag((x + y)*I) == (0, x + y)
    assert match_real_imag(Rational(-2, 3)*i*I) == (None, None)
    assert match_real_imag(1 - 2*i) == (None, None)
    assert match_real_imag(sqrt(2)*(3 - 5*I)) == (None, None)

