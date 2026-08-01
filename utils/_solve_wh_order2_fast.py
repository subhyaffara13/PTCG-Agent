
def _solve_WH_order2_fast(y, lamb):
    """Efficiently solve WH of order 2 according to Weinert.

    Needs order = 2 and n >= 3 (data points).

    Weinert (2007)
    "Efficient computation for Whittaker-Henderson smoothing".
    Computational Statistics and Data Analysis 52:959-74.
    https://doi.org/10.1016/j.csda.2006.11.038
    """
    n = y.shape[0]
    # Convert penalty to convention of Weinert (2007), i.e. A = lambda I + D'D.
    # Note that Weinert denotes the difference matrix M instead of D.
    lamb = 1 / lamb
    # A = LDL' decompositon, i.e. L is unit lower triangular and banded
    # (bandwith=2) and D diagonal.
    # First subdiagonal of L is (-e_1, .., -e_{n-1}) and 2nd subdiagonal
    # (f_1, .., f_{n-2}). Diagonal of D is (d_1, .., d_n).
    # The equation A @ x = lamb * y becomes
    # LD @ b = lamb * y  (I)
    # L.T @ x = b        (II)
    # We shift Weinert's 1-based indices to 0-based indices, Eq. 2.2-2.6
    # Solve problem (I)
    b = np.empty(n)
    e = np.empty(n)
    f = np.empty(n)
    # i=0
    d = 1 + lamb
    f[0] = 1 / d
    mu = 2
    e[0] = mu * f[0]
    b[0] = f[0] * lamb * y[0]
    mu_old = mu
    # i=1
    if n == 3:
        d = 4 + lamb - mu_old * e[0]
        mu = 2 - e[0]
    else:
        d = 5 + lamb - mu_old * e[0]
        mu = 4 - e[0]
    f[1] = 1 / d
    e[1] = mu * f[1]
    b[1] = f[1] * (lamb * y[1] + mu_old * b[0])
    mu_old = mu
    for i in range(2, n-2):
        d = 6 + lamb - mu_old * e[i-1] - f[i-2]
        f[i] = 1 / d
        mu = 4 - e[i-1]
        e[i] = mu * f[i]
        b[i] = f[i] * (lamb * y[i] + mu_old * b[i-1] - b[i-2])
        mu_old = mu
    # i=n-2
    if n >= 4:
        i = n - 2
        d = 5 + lamb - mu_old * e[i-1] - f[i-2]
        f[i] = 1 / d
        mu = 2 - e[i-1]
        e[i] = mu * f[i]
        b[i] = f[i] * (lamb * y[i] + mu_old * b[i-1] - b[i-2])
        mu_old = mu
    # i=n-1
    i = n - 1
    d = 1 + lamb - mu_old * e[i-1] - f[i-2]
    f[i] = 1 / d
    b[i] = f[i] * (lamb * y[i] + mu_old * b[i-1] - b[i-2])

    # Solve problem (II)
    x = np.empty(n)
    x[n-1] = b[n-1]
    x[n-2] = b[n-2] + e[n-2] * x[n-1]
    for i in range(n-3, -1, -1):
        x[i] = b[i] + e[i] * x[i+1] - f[i] * x[i+2]
    return x

