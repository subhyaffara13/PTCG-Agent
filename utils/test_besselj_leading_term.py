
def test_besselj_leading_term():
    assert besselj(0, x).as_leading_term(x) == 1
    assert besselj(1, sin(x)).as_leading_term(x) == x/2
    assert besselj(1, 2*sqrt(x)).as_leading_term(x) == sqrt(x)

    # https://github.com/sympy/sympy/issues/21701
    assert (besselj(z, x)/x**z).as_leading_term(x) == 1/(2**z*gamma(z + 1))

