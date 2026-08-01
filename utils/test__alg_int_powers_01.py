
def test_AlgIntPowers_01():
    T = Poly(cyclotomic_poly(5))
    zeta_pow = AlgIntPowers(T)
    raises(ValueError, lambda: zeta_pow[-1])
    for e in range(10):
        a = e % 5
        if a < 4:
            c = zeta_pow[e]
            assert c[a] == 1 and all(c[i] == 0 for i in range(4) if i != a)
        else:
            assert zeta_pow[e] == [-1] * 4

