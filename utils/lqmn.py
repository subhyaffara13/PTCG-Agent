
def lqmn(m, n, z):
    """Sequence of associated Legendre functions of the second kind.

    Computes the associated Legendre function of the second kind of order m and
    degree n, ``Qmn(z)`` = :math:`Q_n^m(z)`, and its derivative, ``Qmn'(z)``.
    Returns two arrays of size ``(m+1, n+1)`` containing ``Qmn(z)`` and
    ``Qmn'(z)`` for all orders from ``0..m`` and degrees from ``0..n``.

    Parameters
    ----------
    m : int
       ``|m| <= n``; the order of the Legendre function.
    n : int
       where ``n >= 0``; the degree of the Legendre function.  Often
       called ``l`` (lower case L) in descriptions of the associated
       Legendre function
    z : array_like, complex
        Input value.

    Returns
    -------
    Qmn_z : (m+1, n+1) array
       Values for all orders 0..m and degrees 0..n
    Qmn_d_z : (m+1, n+1) array
       Derivatives for all orders 0..m and degrees 0..n

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           https://people.sc.fsu.edu/~jburkardt/f77_src/special_functions/special_functions.html

    """
    if not isscalar(m) or (m < 0):
        raise ValueError("m must be a non-negative integer.")
    if not isscalar(n) or (n < 0):
        raise ValueError("n must be a non-negative integer.")

    m, n = int(m), int(n)  # Convert to int to maintain backwards compatibility.
    # Ensure neither m nor n == 0
    mm = max(1, m)
    nn = max(1, n)

    z = np.asarray(z)
    if (not np.issubdtype(z.dtype, np.inexact)):
        z = z.astype(np.float64)

    if np.iscomplexobj(z):
        q = np.empty((mm + 1, nn + 1) + z.shape, dtype=np.complex128)
    else:
        q = np.empty((mm + 1, nn + 1) + z.shape, dtype=np.float64)
    qd = np.empty_like(q)
    if (z.ndim == 0):
        _lqmn(z, out=(q, qd))
    else:
        # new axes must be last for the ufunc
        _lqmn(z,
              out=(np.moveaxis(q, (0, 1), (-2, -1)),
                   np.moveaxis(qd, (0, 1), (-2, -1))))

    return q[:(m+1), :(n+1)], qd[:(m+1), :(n+1)]

