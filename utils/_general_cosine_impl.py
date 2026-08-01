
def _general_cosine_impl(M, a, xp, device, sym=True):
    if _len_guards(M):
        return xp.ones(M, dtype=xp.float64, device=device)
    M, needs_trunc = _extend(M, sym)

    fac = xp.linspace(-xp.pi, xp.pi, M, dtype=xp.float64, device=device)
    w = xp.zeros(M, dtype=xp.float64, device=device)
    for k in range(a.shape[0]):
        w += a[k] * xp.cos(k * fac)

    return _truncate(w, needs_trunc)

