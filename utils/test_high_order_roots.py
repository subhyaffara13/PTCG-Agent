
def test_high_order_roots():
    s = x**5 + 4*x**3 + 3*x**2 + Rational(7, 4)
    assert set(solve(s)) == set(Poly(s*4, domain='ZZ').all_roots())

