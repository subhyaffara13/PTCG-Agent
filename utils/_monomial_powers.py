
def _monomial_powers(ndim, degree, xp):
    out = _monomial_powers_impl(ndim, degree)
    out = np.asarray(out, dtype=np.int64)
    if len(out) == 0:
        out = out.reshape(0, ndim)
    return out


def _monomial_powers(ndim, degree, xp):
    out = _monomial_powers_impl(ndim, degree)
    out = xp.asarray(out)
    if out.shape[0] == 0:
        out = xp.reshape(out, (0, ndim))
    return out

