
def residue_reduce(a, d, DE, z=None, invert=True):
    """
    Lazard-Rioboo-Rothstein-Trager resultant reduction.

    Explanation
    ===========

    Given a derivation ``D`` on k(t) and f in k(t) simple, return g
    elementary over k(t) and a Boolean b in {True, False} such that f -
    Dg in k[t] if b == True or f + h and f + h - Dg do not have an
    elementary integral over k(t) for any h in k<t> (reduced) if b ==
    False.

    Returns (G, b), where G is a tuple of tuples of the form (s_i, S_i),
    such that g = Add(*[RootSum(s_i, lambda z: z*log(S_i(z, t))) for
    S_i, s_i in G]). f - Dg is the remaining integral, which is elementary
    only if b == True, and hence the integral of f is elementary only if
    b == True.

    f - Dg is not calculated in this function because that would require
    explicitly calculating the RootSum.  Use residue_reduce_derivation().
    """
    # TODO: Use log_to_atan() from rationaltools.py
    # If r = residue_reduce(...), then the logarithmic part is given by:
    # sum([RootSum(a[0].as_poly(z), lambda i: i*log(a[1].as_expr()).subs(z,
    # i)).subs(t, log(x)) for a in r[0]])

    z = z or Dummy('z')
    a, d = a.cancel(d, include=True)
    a, d = a.to_field().mul_ground(1/d.LC()), d.to_field().mul_ground(1/d.LC())
    kkinv = [1/x for x in DE.T[:DE.level]] + DE.T[:DE.level]

    if a.is_zero:
        return ([], True)
    _, a = a.div(d)

    pz = Poly(z, DE.t)

    Dd = derivation(d, DE)
    q = a - pz*Dd

    if Dd.degree(DE.t) <= d.degree(DE.t):
        r, R = d.resultant(q, includePRS=True)
    else:
        r, R = q.resultant(d, includePRS=True)

    R_map, H = {}, []
    for i in R:
        R_map[i.degree()] = i

    r = Poly(r, z)
    Np, Sp = splitfactor_sqf(r, DE, coefficientD=True, z=z)

    for s, i in Sp:
        if i == d.degree(DE.t):
            s = Poly(s, z).monic()
            H.append((s, d))
        else:
            h = R_map.get(i)
            if h is None:
                continue
            h_lc = Poly(h.as_poly(DE.t).LC(), DE.t, field=True)

            h_lc_sqf = h_lc.sqf_list_include(all=True)

            for a, j in h_lc_sqf:
                h = Poly(h, DE.t, field=True).exquo(Poly(gcd(a, s**j, *kkinv),
                    DE.t))

            s = Poly(s, z).monic()

            if invert:
                h_lc = Poly(h.as_poly(DE.t).LC(), DE.t, field=True, expand=False)
                inv, coeffs = h_lc.as_poly(z, field=True).invert(s), [S.One]

                for coeff in h.coeffs()[1:]:
                    L = reduced(inv*coeff.as_poly(inv.gens), [s])[1]
                    coeffs.append(L.as_expr())

                h = Poly(dict(list(zip(h.monoms(), coeffs))), DE.t)

            H.append((s, h))

    b = not any(cancel(i.as_expr()).has(DE.t, z) for i, _ in Np)

    return (H, b)

