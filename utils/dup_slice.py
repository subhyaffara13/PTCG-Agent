
def dup_slice(f, m, n, K):
    """Take a continuous subsequence of terms of ``f`` in ``K[x]``. """
    k = len(f)

    if k >= m:
        M = k - m
    else:
        M = 0
    if k >= n:
        N = k - n
    else:
        N = 0

    f = f[N:M]

    while f and f[0] == K.zero:
        f.pop(0)

    if not f:
        return []
    else:
        return f + [K.zero]*m

