
def _factorialx_approx_core(n, k, extend):
    """
    Core approximation to multifactorial for array n and integer k.
    """
    if k == 1:
        # shortcut for k=1; same for both extensions, because we assume the
        # handling of extend == 'zero' happens in _factorialx_array_approx
        result = _gamma1p(n)
        if isinstance(n, np.ndarray):
            # gamma does not maintain 0-dim arrays; fix it
            result = np.array(result)
        return result

    if extend == "complex":
        # see https://numpy.org/doc/stable/reference/generated/numpy.power.html
        p_dtype = complex if (_is_subdtype(type(k), "c") or k < 0) else None
        with warnings.catch_warnings():
            # do not warn about 0 * inf, nan / nan etc.; the results are correct
            warnings.simplefilter("ignore", RuntimeWarning)
            # don't use `(n-1)/k` in np.power; underflows if 0 is of a uintX type
            result = np.power(k, n / k, dtype=p_dtype) * _gamma1p(n / k)
            result *= rgamma(1 / k + 1) / np.power(k, 1 / k, dtype=p_dtype)
        if isinstance(n, np.ndarray):
            # ensure we keep array-ness for 0-dim inputs; already n/k above loses it
            result = np.array(result)
        return result

    # at this point we are guaranteed that extend='zero' and that k>0 is an integer
    n_mod_k = n % k
    # scalar case separately, unified handling would be inefficient for arrays;
    # don't use isscalar due to numpy/numpy#23574; 0-dim arrays treated below
    if not isinstance(n, np.ndarray):
        with warnings.catch_warnings():
            # large n cause overflow warnings, but infinity is fine
            warnings.simplefilter("ignore", RuntimeWarning)
            return (
                np.power(k, (n - n_mod_k) / k)
                * gamma(n / k + 1) / gamma(n_mod_k / k + 1)
                * max(n_mod_k, 1)
            )

    # factor that's independent of the residue class (see factorialk docstring)
    with warnings.catch_warnings():
        # large n cause overflow warnings, but infinity is fine
        warnings.simplefilter("ignore", RuntimeWarning)
        result = np.power(k, n / k) * gamma(n / k + 1)
    # factor dependent on residue r (for `r=0` it's 1, so we skip `r=0`
    # below and thus also avoid evaluating `max(r, 1)`)
    def corr(k, r): return np.power(k, -r / k) / gamma(r / k + 1) * r
    for r in np.unique(n_mod_k):
        if r == 0:
            continue
        # cast to int because uint types break on `-r`
        result[n_mod_k == r] *= corr(k, int(r))
    return result

