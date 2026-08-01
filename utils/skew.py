
def skew(a, axis=0, bias=True):
    """
    Computes the skewness of a data set.

    Parameters
    ----------
    a : ndarray
        data
    axis : int or None, optional
        Axis along which skewness is calculated. Default is 0.
        If None, compute over the whole array `a`.
    bias : bool, optional
        If False, then the calculations are corrected for statistical bias.

    Returns
    -------
    skewness : ndarray
        The skewness of values along an axis, returning 0 where all values are
        equal.

    Notes
    -----
    For more details about `skew`, see `scipy.stats.skew`.

    """
    a, axis = _chk_asarray(a,axis)
    mean = a.mean(axis, keepdims=True)
    m2 = _moment(a, 2, axis, mean=mean)
    m3 = _moment(a, 3, axis, mean=mean)
    zero = (m2 <= (np.finfo(m2.dtype).resolution * mean.squeeze(axis))**2)
    with np.errstate(all='ignore'):
        vals = ma.where(zero, 0, m3 / m2**1.5)

    if not bias and zero is not ma.masked and m2 is not ma.masked:
        n = a.count(axis)
        can_correct = ~zero & (n > 2)
        if can_correct.any():
            n = np.extract(can_correct, n)
            m2 = np.extract(can_correct, m2)
            m3 = np.extract(can_correct, m3)
            nval = ma.sqrt((n-1.0)*n)/(n-2.0)*m3/m2**1.5
            np.place(vals, can_correct, nval)
    return vals


def skew(a, axis=0, bias=True, nan_policy='propagate'):
    r"""Compute the sample skewness of a data set.

    For normally distributed data, the skewness should be about zero. For
    unimodal continuous distributions, a skewness value greater than zero means
    that there is more weight in the right tail of the distribution. The
    function `skewtest` can be used to determine if the skewness value
    is close enough to zero, statistically speaking.

    Parameters
    ----------
    a : ndarray
        Input array.
    axis : int or None, optional
        Axis along which skewness is calculated. Default is 0.
        If None, compute over the whole array `a`.
    bias : bool, optional
        If False, then the calculations are corrected for statistical bias.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    Returns
    -------
    skewness : ndarray
        The skewness of values along an axis, returning NaN where all values
        are equal.

    Notes
    -----
    The sample skewness is computed as the Fisher-Pearson coefficient
    of skewness, i.e.

    .. math::

        g_1=\frac{m_3}{m_2^{3/2}}

    where

    .. math::

        m_i=\frac{1}{N}\sum_{n=1}^N(x[n]-\bar{x})^i

    is the biased sample :math:`i\texttt{th}` central moment, and
    :math:`\bar{x}` is
    the sample mean.  If ``bias`` is False, the calculations are
    corrected for bias and the value computed is the adjusted
    Fisher-Pearson standardized moment coefficient, i.e.

    .. math::

        G_1=\frac{k_3}{k_2^{3/2}}=
            \frac{\sqrt{N(N-1)}}{N-2}\frac{m_3}{m_2^{3/2}}.

    References
    ----------
    .. [1] Zwillinger, D. and Kokoska, S. (2000). CRC Standard
       Probability and Statistics Tables and Formulae. Chapman & Hall: New
       York. 2000.
       Section 2.2.24.1

    Examples
    --------
    >>> from scipy.stats import skew
    >>> skew([1, 2, 3, 4, 5])
    0.0
    >>> skew([2, 8, 0, 4, 1, 9, 9, 0])
    0.2650554122698573

    """
    xp = array_namespace(a)
    a, axis = _chk_asarray(a, axis, xp=xp)
    n = _count_nonmasked(a, axis, xp=xp)

    mean = xp.mean(a, axis=axis, keepdims=True)
    mean_reduced = xp.squeeze(mean, axis=axis)  # needed later
    m2 = _moment(a, 2, axis, center=mean, xp=xp)
    m3 = _moment(a, 3, axis, center=mean, xp=xp)
    with np.errstate(all='ignore'):
        eps = xp.finfo(m2.dtype).eps
        zero = m2 <= (eps * mean_reduced)**2
        vals = xp.where(zero, xp.nan, m3 / m2**1.5)
    if not bias:
        can_correct = ~zero & (n > 2)
        if is_lazy_array(can_correct) or xp.any(can_correct):
            nval = ((n - 1.0) * n)**0.5 / (n - 2.0) * m3 / m2**1.5
            vals = xp.where(can_correct, nval, vals)

    return vals[()] if vals.ndim == 0 else vals

