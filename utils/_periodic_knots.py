
def _periodic_knots(x, k):
    '''
    returns vector of nodes on circle
    '''
    xc = np.copy(x)
    n = len(xc)
    if k % 2 == 0:
        dx = np.diff(xc)
        xc[1: -1] -= dx[:-1] / 2
    dx = np.diff(xc)
    t = np.zeros(n + 2 * k)
    t[k: -k] = xc
    for i in range(0, k):
        # filling first `k` elements in descending order
        t[k - i - 1] = t[k - i] - dx[-(i % (n - 1)) - 1]
        # filling last `k` elements in ascending order
        t[-k + i] = t[-k + i - 1] + dx[i % (n - 1)]
    return t

