
def _factorialx_array_approx(n, k, extend):
    """
    Calculate approximation to multifactorial for array n and integer k.

    Ensure that values aren't calculated unnecessarily.
    """
    if extend == "complex":
        return _factorialx_approx_core(n, k=k, extend=extend)

    # at this point we are guaranteed that extend='zero' and that k>0 is an integer
    result = zeros(n.shape)
    # keep nans as nans
    place(result, np.isnan(n), np.nan)
    # only compute where n >= 0 (excludes nans), everything else is 0
    cond = (n >= 0)
    n_to_compute = extract(cond, n)
    place(result, cond, _factorialx_approx_core(n_to_compute, k=k, extend=extend))
    return result

