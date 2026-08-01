
def test_poly_gens():
    assert solveset_real(4**(2*(x**2) + 2*x) - 8, x) == \
        FiniteSet(Rational(-3, 2), S.Half)

