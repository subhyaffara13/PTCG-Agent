
def sos2tf(sos):
    r"""
    Return a single transfer function from a series of second-order sections.

    Parameters
    ----------
    sos : array_like
        Array of second-order filter coefficients, must have shape
        ``(n_sections, 6)``. See `sosfilt` for the SOS filter format
        specification.

    Returns
    -------
    b : ndarray
        Numerator polynomial coefficients.
    a : ndarray
        Denominator polynomial coefficients.

    Notes
    -----
    .. versionadded:: 0.16.0

    Examples
    --------
    Find the polynomial representation of an elliptic filter
    using its 'sos' (second-order sections) format.

    >>> from scipy.signal import sos2tf
    >>> from scipy import signal
    >>> sos = signal.ellip(1, 0.001, 50, 0.1, output='sos')
    >>> sos2tf(sos)
    (   array([0.91256522, 0.91256522, 0.        ]),
        array([1.        , 0.82513043, 0.        ]))
    """
    xp = array_namespace(sos)
    sos = xp.asarray(sos)

    result_type = sos.dtype
    if xp.isdtype(result_type, 'integral'):
        result_type = xp_default_dtype(xp)

    b = xp.asarray([1], dtype=result_type)
    a = xp.asarray([1], dtype=result_type)

    n_sections = sos.shape[0]
    for section in range(n_sections):
        b = _pu.polymul(b, sos[section, :3], xp=xp)
        a = _pu.polymul(a, sos[section, 3:], xp=xp)
    return b, a

