
def _pval_cvm_2samp_exact(s, m, n):
    """
    Compute the exact p-value of the Cramer-von Mises two-sample test
    for a given value s of the test statistic.
    m and n are the sizes of the samples.

    [1] Y. Xiao, A. Gordon, and A. Yakovlev, "A C++ Program for
        the Cramér-Von Mises Two-Sample Test", J. Stat. Soft.,
        vol. 17, no. 8, pp. 1-15, Dec. 2006.
    [2] T. W. Anderson "On the Distribution of the Two-Sample Cramer-von Mises
        Criterion," The Annals of Mathematical Statistics, Ann. Math. Statist.
        33(3), 1148-1159, (September, 1962)
    """

    # [1, p. 3]
    m, n = int(m), int(n)
    lcm = np.lcm(m, n)
    # [1, p. 4], below eq. 3
    a = lcm // m
    b = lcm // n
    # Combine Eq. 9 in [2] with Eq. 2 in [1] and solve for $\zeta$
    # Hint: `s` is $U$ in [2], and $T_2$ in [1] is $T$ in [2]
    mn = m * n
    zeta = lcm ** 2 * (m + n) * (6 * s - mn * (4 * mn - 1)) // (6 * mn ** 2)

    # bound maximum value that may appear in `gs` (remember both rows!)
    zeta_bound = lcm**2 * (m + n)  # bound elements in row 1
    combinations = math.comb(m + n, m)  # sum of row 2
    max_gs = max(zeta_bound, combinations)
    dtype = np.min_scalar_type(max_gs)

    # the frequency table of $g_{u, v}^+$ defined in [1, p. 6]
    gs = ([np.array([[0], [1]], dtype=dtype)]
          + [np.empty((2, 0), dtype=dtype) for _ in range(m)])
    for u in range(n + 1):
        next_gs = []
        tmp = np.empty((2, 0), dtype=dtype)
        for v, g in enumerate(gs):
            # Calculate g recursively with eq. 11 in [1]. Even though it
            # doesn't look like it, this also does 12/13 (all of Algorithm 1).
            vi, i0, i1 = np.intersect1d(tmp[0], g[0], return_indices=True)
            tmp = np.concatenate([
                np.stack([vi, tmp[1, i0] + g[1, i1]]),
                np.delete(tmp, i0, 1),
                np.delete(g, i1, 1)
            ], 1)
            res = (a * v - b * u) ** 2
            tmp[0] += res.astype(dtype)
            next_gs.append(tmp)
        gs = next_gs
    value, freq = gs[m]
    return np.float64(np.sum(freq[value >= zeta]) / combinations)

