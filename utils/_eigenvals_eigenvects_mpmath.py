
def _eigenvals_eigenvects_mpmath(M):
    norm2 = lambda v: mp.sqrt(sum(i**2 for i in v))

    v1 = None
    prec = max(x._prec for x in M.atoms(Float))
    eps = 2**-prec

    while prec < DEFAULT_MAXPREC:
        with workprec(prec):
            A = mp.matrix(M.evalf(n=prec_to_dps(prec)))
            E, ER = mp.eig(A)
            v2 = norm2([i for e in E for i in (mp.re(e), mp.im(e))])
            if v1 is not None and mp.fabs(v1 - v2) < eps:
                return E, ER
            v1 = v2
        prec *= 2

    # we get here because the next step would have taken us
    # past MAXPREC or because we never took a step; in case
    # of the latter, we refuse to send back a solution since
    # it would not have been verified; we also resist taking
    # a small step to arrive exactly at MAXPREC since then
    # the two calculations might be artificially close.
    raise PrecisionExhausted

