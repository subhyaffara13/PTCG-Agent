
def test_leading_terms():
    assert sin(1/x).as_leading_term(x) == AccumBounds(-1, 1)
    assert sin(S.Half).as_leading_term(x) == sin(S.Half)
    assert cos(1/x).as_leading_term(x) == AccumBounds(-1, 1)
    assert cos(S.Half).as_leading_term(x) == cos(S.Half)
    assert sec(1/x).as_leading_term(x) == AccumBounds(S.NegativeInfinity, S.Infinity)
    assert csc(1/x).as_leading_term(x) == AccumBounds(S.NegativeInfinity, S.Infinity)
    assert tan(1/x).as_leading_term(x) == AccumBounds(S.NegativeInfinity, S.Infinity)
    assert cot(1/x).as_leading_term(x) == AccumBounds(S.NegativeInfinity, S.Infinity)

    # https://github.com/sympy/sympy/issues/21038
    f = sin(pi*(x + 4))/(3*x)
    assert f.as_leading_term(x) == pi/3

