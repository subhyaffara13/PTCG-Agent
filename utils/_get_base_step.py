import math


def _get_base_step(dtype, xp):
    # Compute the base step length for the provided dtype. Theoretically, the
    # Euler-Maclaurin sum is infinite, but it gets cut off when either the
    # weights underflow or the abscissae cannot be distinguished from the
    # limits of integration. The latter happens to occur first for float32 and
    # float64, and it occurs when `xjc` (the abscissa complement)
    # in `_compute_pair` underflows. We can solve for the argument `tmax` at
    # which it will underflow using [2] Eq. 13.
    fmin = 4*xp.finfo(dtype).smallest_normal  # stay a little away from the limit
    tmax = math.asinh(math.log(2/fmin - 1) / xp.pi)

    # Based on this, we can choose a base step size `h` for level 0.
    # The number of function evaluations will be `2 + m*2^(k+1)`, where `k` is
    # the level and `m` is an integer we get to choose. I choose
    # m = _N_BASE_STEPS = `8` somewhat arbitrarily, but a rationale is that a
    # power of 2 makes floating point arithmetic more predictable. It also
    # results in a base step size close to `1`, which is what [1] uses (and I
    # used here until I found [2] and these ideas settled).
    h0 = tmax / _N_BASE_STEPS
    return xp.asarray(h0, dtype=dtype)[()]

