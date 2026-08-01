
def quad_to_mpmath(q, ctx=None):
    """Turn the quad returned by ``evalf`` into an ``mpf`` or ``mpc``. """
    mpc = make_mpc if ctx is None else ctx.make_mpc
    mpf = make_mpf if ctx is None else ctx.make_mpf
    if q is S.ComplexInfinity:
        raise NotImplementedError
    re, im, _, _ = q
    if im:
        if not re:
            re = fzero
        return mpc((re, im))
    elif re:
        return mpf(re)
    else:
        return mpf(fzero)

