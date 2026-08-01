
def test_decomp_4():
    T = Poly(x ** 2 - 21)
    rad = {}
    ZK, dK = round_two(T, radicals=rad)
    # 21 is 1 mod 4, so field disc is 3*7, and theory says the
    # rational primes 3, 7 should be the square of a prime ideal.
    for p in [3, 7]:
        P = prime_decomp(p, T, dK=dK, ZK=ZK, radical=rad.get(p))
        assert len(P) == 1
        assert P[0].e == 2
        assert P[0]**2 == p*ZK

