
def _trial(factors, n, candidates, verbose=False):
    """
    Helper function for integer factorization. Trial factors ``n`
    against all integers given in the sequence ``candidates``
    and updates the dict ``factors`` in-place. Returns the reduced
    value of ``n`` and a flag indicating whether any factors were found.
    """
    if verbose:
        factors0 = list(factors.keys())
    nfactors = len(factors)
    for d in candidates:
        if n % d == 0:
            if n != d:
                factor_cache[n] = d
            n, m = remove(n // d, d)
            factors[d] = m + 1
    if verbose:
        for k in sorted(set(factors).difference(set(factors0))):
            print(factor_msg % (k, factors[k]))
    return int(n), len(factors) != nfactors

