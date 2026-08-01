
def _get_wilcoxon_distr(n):
    """
    Distribution of probability of the Wilcoxon ranksum statistic r_plus (sum
    of ranks of positive differences).
    Returns an array with the probabilities of all the possible ranks
    r = 0, ..., n*(n+1)/2
    """
    c = np.ones(1, dtype=np.float64)
    for k in range(1, n + 1):
        prev_c = c
        c = np.zeros(k * (k + 1) // 2 + 1, dtype=np.float64)
        m = len(prev_c)
        c[:m] = prev_c * 0.5
        c[-m:] += prev_c * 0.5
    return c

