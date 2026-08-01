
def _to_banded(n_below, n_above, a):
    n = a.shape[0]
    rows = n_above + n_below + 1
    ab = np.zeros((rows, n), dtype=a.dtype)
    ab[n_above] = np.diag(a)
    for i in range(1, n_above + 1):
        ab[n_above - i, i:] = np.diag(a, i)
    for i in range(1, n_below + 1):
        ab[n_above + i, :-i] = np.diag(a, -i)
    return ab

