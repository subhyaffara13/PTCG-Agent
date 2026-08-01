
def test_decomp_7():
    # Try working through an AlgebraicField
    T = Poly(x ** 3 + x ** 2 - 2 * x + 8)
    K = QQ.alg_field_from_poly(T)
    p = 2
    P = K.primes_above(p)
    ZK = K.maximal_order()
    assert len(P) == 3
    assert all(Pi.e == Pi.f == 1 for Pi in P)
    assert prod(Pi**Pi.e for Pi in P) == p*ZK

