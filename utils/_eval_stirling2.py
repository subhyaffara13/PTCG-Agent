
def _eval_stirling2(n, k):
    if n == k == 0:
        return S.One
    if 0 in (n, k):
        return S.Zero

    # some special values
    if n == k:
        return S.One
    elif k == n - 1:
        return binomial(n, 2)
    elif k == 1:
        return S.One
    elif k == 2:
        return Integer(2**(n - 1) - 1)

    return _stirling2(n, k)

