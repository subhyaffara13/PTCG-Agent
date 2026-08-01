
def _anderson_ksamp_continuous(samples, Z, Zstar, k, n, N):
    """Compute A2akN equation 3 of Scholz & Stephens.

    Parameters
    ----------
    samples : sequence of 1-D array_like
        Array of sample arrays.
    Z : array_like
        Sorted array of all observations.
    Zstar : array_like
        Sorted array of unique observations. Unused.
    k : int
        Number of samples.
    n : array_like
        Number of observations in each sample.
    N : int
        Total number of observations.

    Returns
    -------
    A2KN : float
        The A2KN statistics of Scholz and Stephens 1987.

    """
    A2kN = 0.

    j = np.arange(1, N)
    for i in arange(0, k):
        s = np.sort(samples[i])
        Mij = s.searchsorted(Z[:-1], side='right')
        inner = (N*Mij - j*n[i])**2 / (j * (N - j))
        A2kN += inner.sum() / n[i]
    return A2kN / N

