
def _cdf_cvm(x, n=None, *, xp=None):
    """
    Calculate the cdf of the Cramér-von Mises statistic for a finite sample
    size n. If N is None, use the asymptotic cdf (n=inf).

    See equation 1.8 in Csörgő, S. and Faraway, J. (1996) for finite samples,
    1.2 for the asymptotic cdf.

    The function is not expected to be accurate for large values of x, say
    x > 2, when the cdf is very close to 1 and it might return values > 1
    in that case, e.g. _cdf_cvm(2.0, 12) = 1.0000027556716846. Moreover, it
    is not accurate for small values of n, especially close to the bounds of
    the distribution's domain, [1/(12*n), n/3], where the value jumps to 0
    and 1, respectively. These are limitations of the approximation by Csörgő
    and Faraway (1996) implemented in this function.
    """
    xp = array_namespace(x) if xp is None else xp
    x = xp.asarray(x)

    if n is None:
        y = _cdf_cvm_inf(x, xp=xp)
    else:
        # support of the test statistic is [12/n, n/3], see 1.1 in [2]
        y = xp.zeros_like(x, dtype=x.dtype)
        sup = (1./(12*n) < x) & (x < n/3.)
        # note: _psi1_mod does not include the term _cdf_cvm_inf(x) / 12
        # therefore, we need to add it here
        y = xpx.at(y)[sup].set(_cdf_cvm_inf(x[sup], xp=xp) * (1 + 1./(12*n))
                               + _psi1_mod(x[sup], xp=xp) / n)
        y = xpx.at(y)[x >= n/3].set(1.)

    return y[()] if y.ndim == 0 else y

