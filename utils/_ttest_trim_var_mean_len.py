
def _ttest_trim_var_mean_len(a, trim, axis, *, xp):
    """Variance, mean, and length of winsorized input along specified axis"""
    # for use with `ttest_ind` when trimming.
    # further calculations in this test assume that the inputs are sorted.
    # From [4] Section 1 "Let x_1, ..., x_n be n ordered observations..."
    a = xp.sort(a, axis=axis)

    # `g` is the number of elements to be replaced on each tail, converted
    # from a percentage amount of trimming
    n = a.shape[axis]
    g = int(n * trim)

    # Calculate the Winsorized variance of the input samples according to
    # specified `g`
    v = _calculate_winsorized_variance(a, g, axis, xp=xp)

    # the total number of elements in the trimmed samples
    n -= 2 * g

    # calculate the g-times trimmed mean, as defined in [4] (1-1)
    m = trim_mean(a, trim, axis=axis)
    return v, m, n

