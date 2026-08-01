
def obrientransform(*args):
    """
    Computes a transform on input data (any number of columns).  Used to
    test for homogeneity of variance prior to running one-way stats.  Each
    array in ``*args`` is one level of a factor.  If an `f_oneway()` run on
    the transformed data and found significant, variances are unequal.   From
    Maxwell and Delaney, p.112.

    Returns: transformed data for use in an ANOVA
    """  # numpydoc ignore=RT01
    data = argstoarray(*args).T
    v = data.var(axis=0,ddof=1)
    m = data.mean(0)
    n = data.count(0).astype(float)
    # result = ((N-1.5)*N*(a-m)**2 - 0.5*v*(n-1))/((n-1)*(n-2))
    data -= m
    data **= 2
    data *= (n-1.5)*n
    data -= 0.5*v*(n-1)
    data /= (n-1.)*(n-2.)
    if not ma.allclose(v,data.mean(0)):
        raise ValueError("Lack of convergence in obrientransform.")

    return data


def obrientransform(*samples, nan_policy='propagate'):
    """Compute the O'Brien transform on input data (any number of arrays).

    Used to test for homogeneity of variance prior to running one-way stats.
    Each array in ``*samples`` is one level of a factor.
    Significant results of `f_oneway` on the transformed data suggest that the
    variances of the underlying distributions are unequal.
    See Maxwell and Delaney [1]_, p.112.

    Parameters
    ----------
    *samples : array_like
        Any number of arrays.
    nan_policy : {'propagate', 'omit', 'raise'}
        Defines how to handle input NaNs.

        - ``propagate``: if a NaN is present in a sample, all elements of the
          transformed sample will be NaN.
        - ``omit``: NaNs will be omitted when computing reducing statistics for the
          transform, but NaNs in the sample will remain NaNs in the transformed sample.
        - ``raise``: if a NaN is present, a ``ValueError`` will be raised.

    Returns
    -------
    obrientransform : tuple of arrays
        Transformed arrays for use in ANOVA.

    Raises
    ------
    ValueError
        If the mean of the transformed data is not equal to the original
        variance, indicating a lack of convergence in the O'Brien transform.

    References
    ----------
    .. [1] S. E. Maxwell and H. D. Delaney, "Designing Experiments and
           Analyzing Data: A Model Comparison Perspective", Wadsworth, 1990.

    Examples
    --------
    We'll test the following data sets for differences in their variance.

    >>> x = [10, 11, 13, 9, 7, 12, 12, 9, 10]
    >>> y = [13, 21, 5, 10, 8, 14, 10, 12, 7, 15]

    Apply the O'Brien transform to the data.

    >>> from scipy.stats import obrientransform
    >>> tx, ty = obrientransform(x, y)

    Use `scipy.stats.f_oneway` to apply a one-way ANOVA test to the
    transformed data.

    >>> from scipy.stats import f_oneway
    >>> F, p = f_oneway(tx, ty)
    >>> p
    0.1314139477040335

    If we require that ``p < 0.05`` for significance, we cannot conclude
    that the variances are different.

    """
    xp = array_namespace(*samples)
    n_samples = len(samples)
    samples = xp_promote(*samples, force_floating=True, xp=xp)
    samples = (samples,) if n_samples == 1 else samples
    return tuple(_xp_obrientransform_one_sample(sample, xp=xp, nan_policy=nan_policy)
                 for sample in samples)

