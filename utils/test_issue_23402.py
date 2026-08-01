
def test_issue_23402():
    k = QQ.alg_field_from_poly(Poly(x ** 3 + x ** 2 - 2 * x + 8))
    P = k.primes_above(3)
    assert P[0].alpha.equiv(0)

