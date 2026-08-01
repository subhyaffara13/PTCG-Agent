
def sigmaclip(a, low=4., high=4., *, nan_policy='propagate'):
    """Perform iterative sigma-clipping of array elements.

    Starting from the full sample, all elements outside the critical range are
    removed, i.e. all elements of the input array `c` that satisfy either of
    the following conditions::

        c < mean(c) - std(c)*low
        c > mean(c) + std(c)*high

    The iteration continues with the updated sample until no
    elements are outside the (updated) range.

    Parameters
    ----------
    a : array_like
        Data array, will be raveled if not 1-D.
    low : float, optional
        Lower bound factor of sigma clipping. Default is 4.
    high : float, optional
        Upper bound factor of sigma clipping. Default is 4.
    nan_policy : {'propagate', 'omit', 'raise'}
        Defines how to handle input NaNs.

        - ``propagate``: if a NaN is present in the input, the clipped array will be
          empty, and the upper and lower thresholds will be NaN.
        - ``omit``: NaNs will be omitted when performing the calculation.
        - ``raise``: if a NaN is present, a ``ValueError`` will be raised.

    Returns
    -------
    clipped : ndarray
        Input array with clipped elements removed.
    lower : float
        Lower threshold value use for clipping.
    upper : float
        Upper threshold value use for clipping.

    Notes
    -----
    This function iteratively *removes* observations. Once observations are
    removed, they are not re-added in subsequent iterations. Consequently,
    although it is often the case that ``clipped`` is identical to
    ``a[(a >= lower) & (a <= upper)]``, this property is not guaranteed to be
    satisfied; ``clipped`` may have fewer elements.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats import sigmaclip
    >>> a = np.concatenate((np.linspace(9.5, 10.5, 31),
    ...                     np.linspace(0, 20, 5)))
    >>> fact = 1.5
    >>> c, low, upp = sigmaclip(a, fact, fact)
    >>> c
    array([  9.96666667,  10.        ,  10.03333333,  10.        ])
    >>> c.var(), c.std()
    (0.00055555555555555165, 0.023570226039551501)
    >>> low, c.mean() - fact*c.std(), c.min()
    (9.9646446609406727, 9.9646446609406727, 9.9666666666666668)
    >>> upp, c.mean() + fact*c.std(), c.max()
    (10.035355339059327, 10.035355339059327, 10.033333333333333)

    >>> a = np.concatenate((np.linspace(9.5, 10.5, 11),
    ...                     np.linspace(-100, -50, 3)))
    >>> c, low, upp = sigmaclip(a, 1.8, 1.8)
    >>> (c == np.linspace(9.5, 10.5, 11)).all()
    True

    """
    xp = array_namespace(a)
    c = xp_ravel(xp.asarray(a))
    contains_nan = _contains_nan(c, nan_policy, xp_omit_okay=True)
    if contains_nan:
        if nan_policy == 'propagate':
            NaN = _get_nan(c, xp=xp)
            clipped = xp.empty_like(c[0:0])
            return SigmaclipResult(clipped, NaN, NaN)
        elif nan_policy == 'omit':
            c = c[~xp.isnan(c)]

    delta = 1
    while delta:
        c_std = xp.std(c)
        c_mean = xp.mean(c)
        size = xp_size(c)
        critlower = c_mean - c_std * low
        critupper = c_mean + c_std * high
        c = c[(c >= critlower) & (c <= critupper)]
        delta = size - xp_size(c)

    return SigmaclipResult(c, critlower, critupper)

