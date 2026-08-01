
def disc_naive(t, k):
    """Straitforward way to compute the discontinuity matrix. For testing ONLY.

    This routine returns a dense matrix, while `_fitpack_repro.disc` returns
    a packed one.
    """
    n = t.shape[0]

    delta = t[n - k - 1] - t[k]
    nrint = n - 2*k - 1

    ti = t[k+1:n-k-1]   # internal knots
    tii = np.repeat(ti, 2)
    tii[::2] += 1e-10
    tii[1::2] -= 1e-10
    m = BSpline(t, np.eye(n - k - 1), k)(tii, nu=k)

    matr = np.empty((nrint-1, m.shape[1]), dtype=float)
    for i in range(0, m.shape[0], 2):
        matr[i//2, :] = m[i, :] - m[i+1, :]

    matr *= (delta/nrint)**k / math.factorial(k)
    return matr

