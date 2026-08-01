
def _exp1(p, x, prec):
    r"""Helper function for `rs\_exp`. """
    R = p.ring
    p1 = R(1)
    for precx in _giant_steps(prec):
        pt = p - rs_log(p1, x, precx)
        tmp = rs_mul(pt, p1, x, precx)
        p1 += tmp
    return p1

