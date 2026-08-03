import math


def _cdf_cvm_inf(x, *, xp=None):
    """
    Calculate the cdf of the Cramér-von Mises statistic (infinite sample size).

    See equation 1.2 in Csörgő, S. and Faraway, J. (1996).

    Implementation based on MAPLE code of Julian Faraway and R code of the
    function pCvM in the package goftest (v1.1.1), permission granted
    by Adrian Baddeley. Main difference in the implementation: the code
    here keeps adding terms of the series until the terms are small enough.

    The function is not expected to be accurate for large values of x, say
    x > 4, when the cdf is very close to 1.
    """
    xp = array_namespace(x) if xp is None else xp
    x = xp.asarray(x)

    def term(x, k):
        # this expression can be found in [2], second line of (1.3)
        u = math.exp(gammaln(k + 0.5) - gammaln(k+1)) / (xp.pi**1.5 * xp.sqrt(x))
        y = 4*k + 1
        q = y**2 / (16*x)
        b = xp.asarray(kv(0.25, np.asarray(q)), dtype=u.dtype)  # not automatic?
        return u * math.sqrt(y) * xp.exp(-q) * b

    tot = xp.zeros_like(x, dtype=x.dtype)
    cond = xp.ones_like(x, dtype=xp.bool)
    k = 0
    while xp.any(cond):
        z = term(x[cond], k)
        # tot[cond] = tot[cond] + z
        tot = xpx.at(tot)[cond].add(z)
        # cond[cond] = np.abs(z) >= 1e-7
        cond = xpx.at(cond)[xp_copy(cond)].set(xp.abs(z) >= 1e-7)  # torch needs copy
        k += 1

    return tot

