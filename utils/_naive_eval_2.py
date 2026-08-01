
def _naive_eval_2(x, t, c, k, *, xp):
    """Naive B-spline evaluation, another way."""
    n = t.shape[0] - (k+1)
    assert n >= k+1
    assert c.shape[0] >= n
    assert t[k] <= x <= t[n]
    return sum(c[i] * _naive_B(x, k, i, t) for i in range(n))

