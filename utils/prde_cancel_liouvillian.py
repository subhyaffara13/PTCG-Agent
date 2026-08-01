
def prde_cancel_liouvillian(b, Q, n, DE):
    """
    Pg, 237.
    """
    H = []

    # Why use DecrementLevel? Below line answers that:
    # Assuming that we can solve such problems over 'k' (not k[t])
    if DE.case == 'primitive':
        with DecrementLevel(DE):
            ba, bd = frac_in(b, DE.t, field=True)

    for i in range(n, -1, -1):
        if DE.case == 'exp': # this re-checking can be avoided
            with DecrementLevel(DE):
                ba, bd = frac_in(b + (i*(derivation(DE.t, DE)/DE.t)).as_poly(b.gens),
                                DE.t, field=True)
        with DecrementLevel(DE):
            Qy = [frac_in(q.nth(i), DE.t, field=True) for q in Q]
            fi, Ai = param_rischDE(ba, bd, Qy, DE)
        fi = [Poly(fa.as_expr()/fd.as_expr(), DE.t, field=True)
                for fa, fd in fi]
        Ai = Ai.set_gens(DE.t)

        ri = len(fi)

        if i == n:
            M = Ai
        else:
            M = Ai.col_join(M.row_join(zeros(M.rows, ri, DE.t)))

        Fi, hi = [None]*ri, [None]*ri

        # from eq. on top of p.238 (unnumbered)
        for j in range(ri):
            hji = fi[j] * (DE.t**i).as_poly(fi[j].gens)
            hi[j] = hji
            # building up Sum(djn*(D(fjn*t^n) - b*fjnt^n))
            Fi[j] = -(derivation(hji, DE) - b*hji)

        H += hi
        # in the next loop instead of Q it has
        # to be Q + Fi taking its place
        Q = Q + Fi

    return (H, M)

