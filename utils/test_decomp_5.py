
def test_decomp_5():
    # Here is our first test of the "hard case" of prime decomposition.
    # We work in a quadratic extension Q(sqrt(d)) where d is 1 mod 4, and
    # we consider the factorization of the rational prime 2, which divides
    # the index.
    # Theory says the form of p's factorization depends on the residue of
    # d mod 8, so we consider both cases, d = 1 mod 8 and d = 5 mod 8.
    for d in [-7, -3]:
        T = Poly(x ** 2 - d)
        rad = {}
        ZK, dK = round_two(T, radicals=rad)
        p = 2
        P = prime_decomp(p, T, dK=dK, ZK=ZK, radical=rad.get(p))
        if d % 8 == 1:
            assert len(P) == 2
            assert all(P[i].e == 1 and P[i].f == 1 for i in range(2))
            assert prod(Pi**Pi.e for Pi in P) == p * ZK
        else:
            assert d % 8 == 5
            assert len(P) == 1
            assert P[0].e == 1
            assert P[0].f == 2
            assert P[0].as_submodule() == p * ZK

