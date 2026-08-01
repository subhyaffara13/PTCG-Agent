
def field_isomorphism_pslq(a, b):
    """Construct field isomorphism using PSLQ algorithm. """
    if not a.root.is_real or not b.root.is_real:
        raise NotImplementedError("PSLQ doesn't support complex coefficients")

    f = a.minpoly
    g = b.minpoly.replace(f.gen)

    n, m, prev = 100, b.minpoly.degree(), None
    ctx = MPContext()

    for i in range(1, 5):
        A = a.root.evalf(n)
        B = b.root.evalf(n)

        basis = [1, B] + [ B**i for i in range(2, m) ] + [-A]

        ctx.dps = n
        coeffs = ctx.pslq(basis, maxcoeff=10**10, maxsteps=1000)

        if coeffs is None:
            # PSLQ can't find an integer linear combination. Give up.
            break

        if coeffs != prev:
            prev = coeffs
        else:
            # Increasing precision didn't produce anything new. Give up.
            break

        # We have
        #   c0 + c1*B + c2*B^2 + ... + cm-1*B^(m-1) - cm*A ~ 0.
        # So bring cm*A to the other side, and divide through by cm,
        # for an approximate representation of A as a polynomial in B.
        # (We know cm != 0 since `b.minpoly` is irreducible.)
        coeffs = [S(c)/coeffs[-1] for c in coeffs[:-1]]

        # Throw away leading zeros.
        while not coeffs[-1]:
            coeffs.pop()

        coeffs = list(reversed(coeffs))
        h = Poly(coeffs, f.gen, domain='QQ')

        # We only have A ~ h(B). We must check whether the relation is exact.
        if f.compose(h).rem(g).is_zero:
            # Now we know that h(b) is in fact equal to _some conjugate of_ a.
            # But from the very precise approximation A ~ h(B) we can assume
            # the conjugate is a itself.
            return coeffs
        else:
            n *= 2

    return None

