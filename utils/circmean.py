
def circmean(samples, high=2*pi, low=0, axis=None, nan_policy='propagate'):
    r"""Compute the circular mean of a sample of angle observations.

    Given :math:`n` angle observations :math:`x_1, \cdots, x_n` measured in
    radians, their *circular mean* is defined by ([1]_, Eq. 2.2.4)

    .. math::

       \mathrm{Arg} \left( \frac{1}{n} \sum_{k=1}^n e^{i x_k} \right)

    where :math:`i` is the imaginary unit and :math:`\mathop{\mathrm{Arg}} z`
    gives the principal value of the argument of complex number :math:`z`,
    restricted to the range :math:`[0,2\pi]` by default.  :math:`z` in the
    above expression is known as the `mean resultant vector`.

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
    circmean : float
        Circular mean, restricted to the range ``[low, high]``.

        If the mean resultant vector is zero, an input-dependent,
        implementation-defined number between ``[low, high]`` is returned.
        If the input array is empty, ``np.nan`` is returned.

    See Also
    --------
    circstd : Circular standard deviation.
    circvar : Circular variance.

    References
    ----------
    .. [1] Mardia, K. V. and Jupp, P. E. *Directional Statistics*.
           John Wiley & Sons, 1999.

    Examples
    --------
    For readability, all angles are printed out in degrees.

    >>> import numpy as np
    >>> from scipy.stats import circmean
    >>> import matplotlib.pyplot as plt
    >>> angles = np.deg2rad(np.array([20, 30, 330]))
    >>> circmean = circmean(angles)
    >>> np.rad2deg(circmean)
    7.294976657784009

    >>> mean = angles.mean()
    >>> np.rad2deg(mean)
    126.66666666666666

    Plot and compare the circular mean against the arithmetic mean.

    >>> plt.plot(np.cos(np.linspace(0, 2*np.pi, 500)),
    ...          np.sin(np.linspace(0, 2*np.pi, 500)),
    ...          c='k')
    >>> plt.scatter(np.cos(angles), np.sin(angles), c='k')
    >>> plt.scatter(np.cos(circmean), np.sin(circmean), c='b',
    ...             label='circmean')
    >>> plt.scatter(np.cos(mean), np.sin(mean), c='r', label='mean')
    >>> plt.legend()
    >>> plt.axis('equal')
    >>> plt.show()

    """
    xp = array_namespace(samples)
    # Needed for non-NumPy arrays to get appropriate NaN result
    # Apparently atan2(0, 0) is 0, even though it is mathematically undefined
    if xp_size(samples) == 0:
        return xp.mean(samples, axis=axis)
    period = high - low
    samples, sin_samp, cos_samp = _circfuncs_common(samples, period, xp=xp)
    sin_sum = xp.sum(sin_samp, axis=axis)
    cos_sum = xp.sum(cos_samp, axis=axis)
    res = xp.atan2(sin_sum, cos_sum)

    res = res[()] if res.ndim == 0 else res
    return (res * (period / (2.0 * pi)) - low) % period + low

