import math


def _psi1_mod(x, *, xp=None):
    """
    psi1 is defined in equation 1.10 in Csörgő, S. and Faraway, J. (1996).
    This implements a modified version by excluding the term V(x) / 12
    (here: _cdf_cvm_inf(x) / 12) to avoid evaluating _cdf_cvm_inf(x)
    twice in _cdf_cvm.

    Implementation based on MAPLE code of Julian Faraway and R code of the
    function pCvM in the package goftest (v1.1.1), permission granted
    by Adrian Baddeley. Main difference in the implementation: the code
    here keeps adding terms of the series until the terms are small enough.
    """
    xp = array_namespace(x) if xp is None else xp

    def _ed2(y):
        z = y**2 / 4
        z_ = np.asarray(z)
        b = xp.asarray(kv(1/4, z_) + kv(3/4, z_))
        return xp.exp(-z) * (y/2)**(3/2) * b / math.sqrt(np.pi)

    def _ed3(y):
        z = y**2 / 4
        z_ = np.asarray(z)
        c = xp.exp(-z) / math.sqrt(np.pi)
        kv_terms = xp.asarray(2*kv(1/4, z_)
                              + 3*kv(3/4, z_) - kv(5/4, z_))
        return c * (y/2)**(5/2) * kv_terms

    def _Ak(k, x):
        m = 2*k + 1
        sx = 2 * xp.sqrt(x)
        y1 = x**(3/4)
        y2 = x**(5/4)

        gamma_kp1_2 = float(gamma(k + 1 / 2))
        gamma_kp3_2 = float(gamma(k + 3 / 2))

        e1 = m * gamma_kp1_2 * _ed2((4 * k + 3)/sx) / (9 * y1)
        e2 = gamma_kp1_2 * _ed3((4 * k + 1) / sx) / (72 * y2)
        e3 = 2 * (m + 2) * gamma_kp3_2 * _ed3((4 * k + 5) / sx) / (12 * y2)
        e4 = 7 * m * gamma_kp1_2 * _ed2((4 * k + 1) / sx) / (144 * y1)
        e5 = 7 * m * gamma_kp1_2 * _ed2((4 * k + 5) / sx) / (144 * y1)

        return e1 + e2 + e3 + e4 + e5

    x = xp.asarray(x)
    tot = xp.zeros_like(x)
    cond = xp.ones_like(x, dtype=xp.bool)
    k = 0
    while xp.any(cond):
        gamma_kp1 = float(gamma(k + 1))
        z = -_Ak(k, x[cond]) / (xp.pi * gamma_kp1)
        tot = xpx.at(tot)[cond].set(tot[cond] + z)
        # For float32 arithmetic, the tolerance may need to be adjusted or the
        # algorithm may prove to be unsuitable.
        cond = xpx.at(cond)[xp_copy(cond)].set(xp.abs(z) >= 1e-7)
        k += 1

    return tot

