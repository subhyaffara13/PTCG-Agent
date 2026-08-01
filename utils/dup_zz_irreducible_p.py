
def dup_zz_irreducible_p(f, K):
    """Test irreducibility using Eisenstein's criterion. """
    lc = dup_LC(f, K)
    tc = dup_TC(f, K)

    e_fc = dup_content(f[1:], K)

    if e_fc:
        from sympy.ntheory import factorint
        e_ff = factorint(int(e_fc))

        for p in e_ff.keys():
            if (lc % p) and (tc % p**2):
                return True

