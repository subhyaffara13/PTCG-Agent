
def circvar(samples, high=2*pi, low=0, axis=None, nan_policy='propagate'):
    r"""Compute the circular variance of a sample of angle observations.

    Given :math:`n` angle observations :math:`x_1, \cdots, x_n` measured in
    radians, their *circular variance* is defined by ([2]_, Eq. 2.3.3)

    .. math::

       1 - \left| \frac{1}{n} \sum_{k=1}^n e^{i x_k} \right|

    where :math:`i` is the imaginary unit and :math:`|z|` gives the length
    of the complex number :math:`z`.  :math:`|z|` in the above expression
    is known as the `mean resultant length`.

    Parameters
    ----------
    samples : array_like
        Input array of angle observations.  The value of a full angle is
        equal to ``(high - low)``.
    high : float, optional
        Upper boundary of the principal value of an angle.  Default is ``2*pi``.
    low : float, optional
        Lower boundary of the principal value of an angle.  Default is ``0``.

    Returns
    -------
    circvar : float
        Circular variance.  The returned value is in the range ``[0, 1]``,
        where ``0`` indicates no variance and ``1`` indicates large variance.

        If the input array is empty, ``np.nan`` is returned.

    See Also
    --------
    circmean : Circular mean.
    circstd : Circular standard deviation.

    Notes
    -----
    In the limit of small angles, the circular variance is close to
    half the 'linear' variance if measured in radians.

    References
    ----------
    .. [1] Fisher, N.I. *Statistical analysis of circular data*. Cambridge
           University Press, 1993.
    .. [2] Mardia, K. V. and Jupp, P. E. *Directional Statistics*.
           John Wiley & Sons, 1999.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats import circvar
    >>> import matplotlib.pyplot as plt
    >>> samples_1 = np.array([0.072, -0.158, 0.077, 0.108, 0.286,
    ...                       0.133, -0.473, -0.001, -0.348, 0.131])
    >>> samples_2 = np.array([0.111, -0.879, 0.078, 0.733, 0.421,
    ...                       0.104, -0.136, -0.867,  0.012,  0.105])
    >>> circvar_1 = circvar(samples_1)
    >>> circvar_2 = circvar(samples_2)

    Plot the samples.

    >>> fig, (left, right) = plt.subplots(ncols=2)
    >>> for image in (left, right):
    ...     image.plot(np.cos(np.linspace(0, 2*np.pi, 500)),
    ...                np.sin(np.linspace(0, 2*np.pi, 500)),
    ...                c='k')
    ...     image.axis('equal')
    ...     image.axis('off')
    >>> left.scatter(np.cos(samples_1), np.sin(samples_1), c='k', s=15)
    >>> left.set_title(f"circular variance: {np.round(circvar_1, 2)!r}")
    >>> right.scatter(np.cos(samples_2), np.sin(samples_2), c='k', s=15)
    >>> right.set_title(f"circular variance: {np.round(circvar_2, 2)!r}")
    >>> plt.show()

    """
    xp = array_namespace(samples)
    period = high - low
    samples, sin_samp, cos_samp = _circfuncs_common(samples, period, xp=xp)
    sin_mean = xp.mean(sin_samp, axis=axis)
    cos_mean = xp.mean(cos_samp, axis=axis)
    hypotenuse = (sin_mean**2. + cos_mean**2.)**0.5
    # hypotenuse can go slightly above 1 due to rounding errors
    R = xp.clip(hypotenuse, max=1.)

    res = 1. - R
    return res

