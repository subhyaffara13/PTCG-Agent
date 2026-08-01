
def test_AlgIntPowers_02():
    T = Poly(x**3 + 2*x**2 + 3*x + 4)
    m = 7
    theta_pow = AlgIntPowers(T, m)
    for e in range(10):
        computed = theta_pow[e]
        coeffs = (Poly(x)**e % T + Poly(x**3)).rep.to_list()[1:]
        expected = [c % m for c in reversed(coeffs)]
        assert computed == expected

