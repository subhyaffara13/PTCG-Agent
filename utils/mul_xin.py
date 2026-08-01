
def mul_xin(p, i, n):
    r"""
    Return `p*x_i**n`.

    `x\_i` is the ith variable in ``p``.
    """
    R = p.ring
    q = {}
    for k, v in p.terms():
        k1 = list(k)
        k1[i] += n
        q[tuple(k1)] = v
    return R(q)

