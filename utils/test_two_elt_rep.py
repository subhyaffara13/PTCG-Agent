
def test_two_elt_rep():
    ell = 7
    T = Poly(cyclotomic_poly(ell))
    ZK, dK = round_two(T)
    for p in [29, 13, 11, 5]:
        P = prime_decomp(p, T)
        for Pi in P:
            # We have Pi in two-element representation, and, because we are
            # looking at a cyclotomic field, this was computed by the "easy"
            # method that just factors T mod p. We will now convert this to
            # a set of Z-generators, then convert that back into a two-element
            # rep. The latter need not be identical to the two-elt rep we
            # already have, but it must have the same HNF.
            H = p*ZK + Pi.alpha*ZK
            gens = H.basis_element_pullbacks()
            # Note: we could supply f = Pi.f, but prefer to test behavior without it.
            b = _two_elt_rep(gens, ZK, p)
            if b != Pi.alpha:
                H2 = p*ZK + b*ZK
                assert H2 == H

