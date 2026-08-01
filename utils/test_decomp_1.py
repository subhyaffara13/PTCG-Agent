
def test_decomp_1():
    # All prime decompositions in cyclotomic fields are in the "easy case,"
    # since the index is unity.
    # Here we check the ramified prime.
    T = Poly(cyclotomic_poly(7))
    raises(ValueError, lambda: prime_decomp(7))
    P = prime_decomp(7, T)
    assert len(P) == 1
    P0 = P[0]
    assert P0.e == 6
    assert P0.f == 1
    # Test powers:
    assert P0**0 == P0.ZK
    assert P0**1 == P0
    assert P0**6 == 7 * P0.ZK

