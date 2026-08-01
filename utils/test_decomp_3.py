
def test_decomp_3():
    T = Poly(x ** 2 - 35)
    rad = {}
    ZK, dK = round_two(T, radicals=rad)
    # 35 is 3 mod 4, so field disc is 4*5*7, and theory says each of the
    # rational primes 2, 5, 7 should be the square of a prime ideal.
    for p in [2, 5, 7]:
        P = prime_decomp(p, T, dK=dK, ZK=ZK, radical=rad.get(p))
        assert len(P) == 1
        assert P[0].e == 2
        assert P[0]**2 == p*ZK

