
def test_decomp_2():
    # More easy cyclotomic cases, but here we check unramified primes.
    ell = 7
    T = Poly(cyclotomic_poly(ell))
    for p in [29, 13, 11, 5]:
        f_exp = n_order(p, ell)
        g_exp = (ell - 1) // f_exp
        P = prime_decomp(p, T)
        assert len(P) == g_exp
        for Pi in P:
            assert Pi.e == 1
            assert Pi.f == f_exp

