
def unit_impulse(shape, idx=None, dtype=float):
    r"""
    Unit impulse signal (discrete delta function) or unit basis vector.

    Parameters
    ----------
    shape : int or tuple of int
        Number of samples in the output (1-D), or a tuple that represents the
        shape of the output (N-D).
    idx : None or int or tuple of int or 'mid', optional
        Index at which the value is 1.  If None, defaults to the 0th element.
        If ``idx='mid'``, the impulse will be centered at ``shape // 2`` in
        all dimensions.  If an int, the impulse will be at `idx` in all
        dimensions.
    dtype : data-type, optional
        The desired data-type for the array, e.g., ``numpy.int8``.  Default is
        ``numpy.float64``.

    Returns
    -------
    y : ndarray
        Output array containing an impulse signal.

    Notes
    -----
    In digital signal processing literature the unit impulse signal is often
    represented by the Kronecker delta. [1]_ I.e., a signal :math:`u_k[n]`,
    which is zero everywhere except being one at the :math:`k`-th sample,
    can be expressed as

    .. math::

        u_k[n] = \delta[n-k] \equiv \delta_{n,k}\ .

    Furthermore, the unit impulse is frequently interpreted as the discrete-time
    version of the continuous-time Dirac distribution. [2]_

    References
    ----------
    .. [1] "Kronecker delta", *Wikipedia*,
           https://en.wikipedia.org/wiki/Kronecker_delta#Digital_signal_processing
    .. [2] "Dirac delta function" *Wikipedia*,
           https://en.wikipedia.org/wiki/Dirac_delta_function#Relationship_to_the_Kronecker_delta

    .. versionadded:: 0.19.0

    Examples
    --------
    An impulse at the 0th element (:math:`\\delta[n]`):

    >>> from scipy import signal
    >>> signal.unit_impulse(8)
    array([ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])

    Impulse offset by 2 samples (:math:`\\delta[n-2]`):

    >>> signal.unit_impulse(7, 2)
    array([ 0.,  0.,  1.,  0.,  0.,  0.,  0.])

    2-dimensional impulse, centered:

    >>> signal.unit_impulse((3, 3), 'mid')
    array([[ 0.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  0.]])

    Impulse at (2, 2), using broadcasting:

    >>> signal.unit_impulse((4, 4), 2)
    array([[ 0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.],
           [ 0.,  0.,  1.,  0.],
           [ 0.,  0.,  0.,  0.]])

    Plot the impulse response of a 4th-order Butterworth lowpass filter:

    >>> imp = signal.unit_impulse(100, 'mid')
    >>> b, a = signal.butter(4, 0.2)
    >>> response = signal.lfilter(b, a, imp)

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> plt.plot(np.arange(-50, 50), imp)
    >>> plt.plot(np.arange(-50, 50), response)
    >>> plt.margins(0.1, 0.1)
    >>> plt.xlabel('Time [samples]')
    >>> plt.ylabel('Amplitude')
    >>> plt.grid(True)
    >>> plt.show()

    """
    out = zeros(shape, dtype)

    shape = np.atleast_1d(shape)

    if idx is None:
        idx = (0,) * len(shape)
    elif idx == 'mid':
        idx = tuple(shape // 2)
    elif not hasattr(idx, "__iter__"):
        idx = (idx,) * len(shape)

    out[idx] = 1
    return out

