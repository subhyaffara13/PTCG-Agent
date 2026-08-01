
def test_limit_seq():
    e = binomial(2*n, n) / Sum(binomial(2*k, k), (k, 1, n))
    assert limit_seq(e) == S(3) / 4
    assert limit_seq(e, m) == e

    e = (5*n**3 + 3*n**2 + 4) / (3*n**3 + 4*n - 5)
    assert limit_seq(e, n) == S(5) / 3

    e = (harmonic(n) * Sum(harmonic(k), (k, 1, n))) / (n * harmonic(2*n)**2)
    assert limit_seq(e, n) == 1

    e = Sum(k**2 * Sum(2**m/m, (m, 1, k)), (k, 1, n)) / (2**n*n)
    assert limit_seq(e, n) == 4

    e = (Sum(binomial(3*k, k) * binomial(5*k, k), (k, 1, n)) /
         (binomial(3*n, n) * binomial(5*n, n)))
    assert limit_seq(e, n) == S(84375) / 83351

    e = Sum(harmonic(k)**2/k, (k, 1, 2*n)) / harmonic(n)**3
    assert limit_seq(e, n) == S.One / 3

    raises(ValueError, lambda: limit_seq(e * m))

