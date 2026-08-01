
def test_decomp_6():
    # Another case where 2 divides the index. This is Dedekind's example of
    # an essential discriminant divisor. (See Cohen, Exercise 6.10.)
    T = Poly(x ** 3 + x ** 2 - 2 * x + 8)
    rad = {}
    ZK, dK = round_two(T, radicals=rad)
    p = 2
    P = prime_decomp(p, T, dK=dK, ZK=ZK, radical=rad.get(p))
    assert len(P) == 3
    assert all(Pi.e == Pi.f == 1 for Pi in P)
    assert prod(Pi**Pi.e for Pi in P) == p*ZK

