
def stirling1(ctx, n, k, exact=False):
    v = ctx._stirling1(int(n), int(k))
    if exact:
        return int(v)
    else:
        return ctx.mpf(v)


def stirling1(n, k):
    """
    Stirling number of the first kind.
    """
    if n < 0 or k < 0:
        raise ValueError
    if k >= n:
        return MPZ(n == k)
    if k < 1:
        return MPZ_ZERO
    L = [MPZ_ZERO] * (k+1)
    L[1] = MPZ_ONE
    for m in xrange(2, n+1):
        for j in xrange(min(k, m), 0, -1):
            L[j] = (m-1) * L[j] + L[j-1]
    return (-1)**(n+k) * L[k]

