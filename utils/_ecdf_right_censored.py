
def _ecdf_right_censored(sample):
    # It is conventional to discuss right-censored data in terms of
    # "survival time", "death", and "loss" (e.g. [2]). We'll use that
    # terminology here.
    # This implementation was influenced by the references cited and also
    # https://www.youtube.com/watch?v=lxoWsVco_iM
    # https://en.wikipedia.org/wiki/Kaplan%E2%80%93Meier_estimator
    # In retrospect it is probably most easily compared against [3].
    # Ultimately, the data needs to be sorted, so this implementation is
    # written to avoid a separate call to `unique` after sorting. In hope of
    # better performance on large datasets, it also computes survival
    # probabilities at unique times only rather than at each observation.
    tod = sample._uncensored  # time of "death"
    tol = sample._right  # time of "loss"
    times = np.concatenate((tod, tol))
    died = np.asarray([1]*tod.size + [0]*tol.size)

    # sort by times
    i = np.argsort(times)
    times = times[i]
    died = died[i]
    at_risk = np.arange(times.size, 0, -1)

    # logical indices of unique times
    j = np.diff(times, prepend=-np.inf, append=np.inf) > 0
    j_l = j[:-1]  # first instances of unique times
    j_r = j[1:]  # last instances of unique times

    # get number at risk and deaths at each unique time
    t = times[j_l]  # unique times
    n = at_risk[j_l]  # number at risk at each unique time
    cd = np.cumsum(died)[j_r]  # cumulative deaths up to/including unique times
    d = np.diff(cd, prepend=0)  # deaths at each unique time

    # compute survival function
    sf = np.cumprod((n - d) / n)
    cdf = 1 - sf
    return t, cdf, sf, n, d

