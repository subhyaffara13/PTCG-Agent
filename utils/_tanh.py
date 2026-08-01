
def _tanh(p, x, prec):
    r"""
    Helper function of :func:`rs_tanh`

    Return the series expansion of tanh of a univariate series using Newton's
    method. It takes advantage of the fact that series expansion of atanh is
    easier than that of tanh.

    See Also
    ========

    _tanh
    """
    R = p.ring
    p1 = R(0)
    for precx in _giant_steps(prec):
        tmp = p - rs_atanh(p1, x, precx)
        tmp = rs_mul(tmp, 1 - rs_square(p1, x, prec), x, precx)
        p1 += tmp
    return p1

