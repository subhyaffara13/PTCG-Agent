
def test_gosper_normal():
    eq = 4*n + 5, 2*(4*n + 1)*(2*n + 3), n
    assert gosper_normal(*eq) == \
        (Poly(Rational(1, 4), n), Poly(n + Rational(3, 2)), Poly(n + Rational(1, 4)))
    assert gosper_normal(*eq, polys=False) == \
        (Rational(1, 4), n + Rational(3, 2), n + Rational(1, 4))

