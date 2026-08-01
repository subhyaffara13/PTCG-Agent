
def tf2sos(b, a, pairing=None, *, analog=False):
    r"""
    Return second-order sections from transfer function representation.

    Parameters
    ----------
    b : array_like, shape (M,)
        Numerator polynomial coefficients. Must be 1-D.
    a : array_like, shape (N,)
        Denominator polynomial coefficients. Must be 1-D.
    pairing : {None, 'nearest', 'keep_odd', 'minimal'}, optional
        The method to use to combine pairs of poles and zeros into sections.
        See `zpk2sos` for information and restrictions on `pairing` and
        `analog` arguments.
    analog : bool, optional
        If True, system is analog, otherwise discrete.

        .. versionadded:: 1.8.0

    Returns
    -------
    sos : ndarray
        Array of second-order filter coefficients, with shape
        ``(n_sections, 6)``. See `sosfilt` for the SOS filter format
        specification.

    See Also
    --------
    zpk2sos, sosfilt

    Notes
    -----
    It is generally discouraged to convert from TF to SOS format, since doing
    so usually will not improve numerical precision errors. Instead, consider
    designing filters in ZPK format and converting directly to SOS. TF is
    converted to SOS by first converting to ZPK format, then converting
    ZPK to SOS.

    .. versionadded:: 0.16.0

    Examples
    --------
    Find the 'sos' (second-order sections) of the transfer function H(s)
    using its polynomial representation.

    .. math::

        H(s) = \frac{s^2 - 3.5s - 2}{s^4 + 3s^3 - 15s^2 - 19s + 30}

    >>> from scipy.signal import tf2sos
    >>> tf2sos([1, -3.5, -2], [1, 3, -15, -19, 30], analog=True)
    array([[  0. ,   0. ,   1. ,   1. ,   2. , -15. ],
           [  1. ,  -3.5,  -2. ,   1. ,   1. ,  -2. ]])
    """
    return zpk2sos(*tf2zpk(b, a), pairing=pairing, analog=analog)

