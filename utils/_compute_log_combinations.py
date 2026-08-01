
def _compute_log_combinations(n):
    """Compute all log combination of C(n, k)."""
    gammaln_arr = gammaln(np.arange(n + 1) + 1)
    return gammaln(n + 1) - gammaln_arr - gammaln_arr[::-1]

