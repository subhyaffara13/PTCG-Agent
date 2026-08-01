
def ifac2(n, memo_pair=[{0:1}, {1:1}]):
    """Return n!! (double factorial), integers n >= 0 only."""
    memo = memo_pair[n&1]
    f = memo.get(n)
    if f:
        return f
    k = max(memo)
    p = memo[k]
    MAX = MAX_FACTORIAL_CACHE
    while k < n:
        k += 2
        p *= k
        if k <= MAX:
            memo[k] = p
    return p

