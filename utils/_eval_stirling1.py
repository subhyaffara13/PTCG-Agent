
def _eval_stirling1(n, k):
    if n == k == 0:
        return S.One
    if 0 in (n, k):
        return S.Zero

    # some special values
    if n == k:
        return S.One
    elif k == n - 1:
        return binomial(n, 2)
    elif k == n - 2:
        return (3*n - 1)*binomial(n, 3)/4
    elif k == n - 3:
        return binomial(n, 2)*binomial(n, 4)

    return _stirling1(n, k)

