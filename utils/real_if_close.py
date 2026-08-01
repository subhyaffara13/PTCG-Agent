
def real_if_close(a: ArrayLike, tol=100):
    if not torch.is_complex(a):
        return a
    if tol > 1:
        # Undocumented in numpy: if tol < 1, it's an absolute tolerance!
        # Otherwise, tol > 1 is relative tolerance, in units of the dtype epsilon
        # https://github.com/numpy/numpy/blob/v1.24.0/numpy/lib/type_check.py#L577
        tol = tol * torch.finfo(a.dtype).eps

    mask = torch.abs(a.imag) < tol
    return a.real if mask.all() else a


def real_if_close(a, tol=100):
    """
    If input is complex with all imaginary parts close to zero, return
    real parts.

    "Close to zero" is defined as `tol` * (machine epsilon of the type for
    `a`).

    Parameters
    ----------
    a : array_like
        Input array.
    tol : float
        Tolerance in machine epsilons for the complex part of the elements
        in the array. If the tolerance is <=1, then the absolute tolerance
        is used.

    Returns
    -------
    out : ndarray
        If `a` is real, the type of `a` is used for the output.  If `a`
        has complex elements, the returned type is float.

    See Also
    --------
    real, imag, angle

    Notes
    -----
    Machine epsilon varies from machine to machine and between data types
    but Python floats on most platforms have a machine epsilon equal to
    2.2204460492503131e-16.  You can use 'np.finfo(float).eps' to print
    out the machine epsilon for floats.

    Examples
    --------
    >>> import numpy as np
    >>> np.finfo(float).eps
    2.2204460492503131e-16 # may vary

    >>> np.real_if_close([2.1 + 4e-14j, 5.2 + 3e-15j], tol=1000)
    array([2.1, 5.2])
    >>> np.real_if_close([2.1 + 4e-13j, 5.2 + 3e-15j], tol=1000)
    array([2.1+4.e-13j, 5.2 + 3e-15j])

    """
    a = asanyarray(a)
    type_ = a.dtype.type
    if not issubclass(type_, _nx.complexfloating):
        return a
    if tol > 1:
        f = getlimits.finfo(type_)
        tol = f.eps * tol
    if _nx.all(_nx.absolute(a.imag) < tol):
        a = a.real
    return a

