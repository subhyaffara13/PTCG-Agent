
def _naive_eval(x, t, c, k, *, xp):
    """
    Naive B-spline evaluation. Useful only for testing!
    """
    if x == t[k]:
        i = k
    else:
        i = xp.searchsorted(t, x) - 1

    assert t[i] <= x <= t[i+1]
    assert i >= k and i < t.shape[0] - k
    return sum(c[i-j] * _naive_B(x, k, i-j, t) for j in range(0, k+1))

