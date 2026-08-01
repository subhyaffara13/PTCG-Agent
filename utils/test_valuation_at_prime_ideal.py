
def test_valuation_at_prime_ideal():
    p = 7
    T = Poly(cyclotomic_poly(p))
    ZK, dK = round_two(T)
    P = prime_decomp(p, T, dK=dK, ZK=ZK)
    assert len(P) == 1
    P0 = P[0]
    v = P0.valuation(p*ZK)
    assert v == P0.e
    # Test easy 0 case:
    assert P0.valuation(5*ZK) == 0

