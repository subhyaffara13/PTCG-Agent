
def _ks_2samp_prob(d, n1, n2, mode, MAX_AUTO_N, alternative):
    # math.gcd used to return an `int`, but now that these return arrays, NumPy can
    # return an int32. Unless we want the pythranized functions to be compiled for
    # int32, this needs to produce an int64.
    g = np.gcd(n1, n2).astype(np.int64)
    n1g = n1 // g
    n2g = n2 // g
    prob = -np.inf
    if mode == 'auto':
        mode = 'exact' if max(n1, n2) <= MAX_AUTO_N else 'asymp'
    elif mode == 'exact':
        # If lcm(n1, n2) is too big, switch from exact to asymp
        if n1g >= np.iinfo(np.int32).max / n2g:
            mode = 'asymp'
            warnings.warn(
                f"Exact ks_2samp calculation not possible with samples sizes "
                f"{n1} and {n2}. Switching to 'asymp'.", RuntimeWarning,
                stacklevel=3)

    if mode == 'exact':
        success, d, prob = _attempt_exact_2kssamp(n1, n2, g, d, alternative)
        if not success:
            mode = 'asymp'
            warnings.warn(f"ks_2samp: Exact calculation unsuccessful. "
                          f"Switching to method={mode}.", RuntimeWarning,
                          stacklevel=3)

    if mode == 'asymp':
        # The product n1*n2 is large.  Use Smirnov's asymptotic formula.
        # Ensure float to avoid overflow in multiplication
        # sorted because the one-sided formula is not symmetric in n1, n2
        m, n = sorted([float(n1), float(n2)], reverse=True)
        en = m * n / (m + n)
        if alternative == 'two-sided':
            prob = distributions.kstwo.sf(d, np.round(en))
        else:
            z = np.sqrt(en) * d
            # Use Hodges' suggested approximation Eqn 5.3
            # Requires m to be the larger of (n1, n2)
            expt = -2 * z**2 - 2 * z * (m + 2*n)/np.sqrt(m*n*(m+n))/3.0
            prob = np.exp(expt)

    prob = np.clip(prob, 0, 1)
    return prob

