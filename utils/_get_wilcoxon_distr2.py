
def _get_wilcoxon_distr2(n):
    """
    Distribution of probability of the Wilcoxon ranksum statistic r_plus (sum
    of ranks of positive differences).
    Returns an array with the probabilities of all the possible ranks
    r = 0, ..., n*(n+1)/2
    This is a slower reference function
    References
    ----------
    .. [1] 1. Harris T, Hardin JW. Exact Wilcoxon Signed-Rank and Wilcoxon
        Mann-Whitney Ranksum Tests. The Stata Journal. 2013;13(2):337-343.
    """
    ai = np.arange(1, n+1)[:, None]
    t = n*(n+1)/2
    q = 2*t
    j = np.arange(q)
    theta = 2*np.pi/q*j
    phi_sp = np.prod(np.cos(theta*ai), axis=0)
    phi_s = np.exp(1j*theta*t) * phi_sp
    p = np.real(ifft(phi_s))
    res = np.zeros(int(t)+1)
    res[:-1:] = p[::2]
    res[0] /= 2
    res[-1] = res[0]
    return res

