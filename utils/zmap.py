
def zmap(scores, compare, axis=0, ddof=0, nan_policy='propagate'):
    """
    Calculate the relative z-scores.

    Return an array of z-scores, i.e., scores that are standardized to
    zero mean and unit variance, where mean and variance are calculated
    from the comparison array.

    Parameters
    ----------
    scores : array_like
        The input for which z-scores are calculated.
    compare : array_like
        The input from which the mean and standard deviation of the
        normalization are taken; assumed to have the same dimension as
        `scores`.
    axis : int or None, optional
        Axis over which mean and variance of `compare` are calculated.
        Default is 0. If None, compute over the whole array `scores`.
    ddof : int, optional
        Degrees of freedom correction in the calculation of the
        standard deviation. Default is 0.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle the occurrence of nans in `compare`.
        'propagate' returns nan, 'raise' raises an exception, 'omit'
        performs the calculations ignoring nan values. Default is
        'propagate'. Note that when the value is 'omit', nans in `scores`
        also propagate to the output, but they do not affect the z-scores
        computed for the non-nan values.

    Returns
    -------
    zscore : array_like
        Z-scores, in the same shape as `scores`.

    Notes
    -----
    This function preserves ndarray subclasses, and works also with
    matrices and masked arrays (it uses `asanyarray` instead of
    `asarray` for parameters).

    Examples
    --------
    >>> from scipy.stats import zmap
    >>> a = [0.5, 2.0, 2.5, 3]
    >>> b = [0, 1, 2, 3, 4]
    >>> zmap(a, b)
    array([-1.06066017,  0.        ,  0.35355339,  0.70710678])

    """
    # The docstring explicitly states that it preserves subclasses.
    # Let's table deprecating that and just get the array API version
    # working.

    like_zscore = (scores is compare)
    xp = array_namespace(scores, compare)
    scores, compare = xp_promote(scores, compare, force_floating=True, xp=xp)

    with warnings.catch_warnings():
        if like_zscore:  # zscore should not emit SmallSampleWarning
            warnings.simplefilter('ignore', SmallSampleWarning)

        mn = _xp_mean(compare, axis=axis, keepdims=True, nan_policy=nan_policy)
        std = _xp_var(compare, axis=axis, correction=ddof,
                      keepdims=True, nan_policy=nan_policy)**0.5

    with np.errstate(invalid='ignore', divide='ignore'):
        z = _demean(scores, mn, axis, xp=xp, precision_warning=False) / std

    # If we know that scores and compare are identical, we can infer that
    # some slices should have NaNs.
    if like_zscore:
        eps = xp.finfo(z.dtype).eps
        zero = std <= xp.abs(eps * mn)
        zero = xp.broadcast_to(zero, z.shape)
        z = xpx.at(z, zero).set(xp.nan)

    return z

