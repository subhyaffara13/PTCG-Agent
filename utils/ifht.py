
def ifht(A, dln, mu, offset=0.0, bias=0.0):
    r"""Compute the inverse fast Hankel transform.

    Computes the discrete inverse Hankel transform of a logarithmically spaced
    periodic sequence. This is the inverse operation to `fht`.

    Parameters
    ----------
    A : array_like (..., n)
        Real periodic input array, uniformly logarithmically spaced.  For
        multidimensional input, the transform is performed over the last axis.
    dln : float
        Uniform logarithmic spacing of the input array.
    mu : float
        Order of the Hankel transform, any positive or negative real number.
    offset : float, optional
        Offset of the uniform logarithmic spacing of the output array.
    bias : float, optional
        Exponent of power law bias, any positive or negative real number.

    Returns
    -------
    a : array_like (..., n)
        The transformed output array, which is real, periodic, uniformly
        logarithmically spaced, and of the same shape as the input array.

    See Also
    --------
    fht : Definition of the fast Hankel transform.
    fhtoffset : Return an optimal offset for `ifht`.

    Notes
    -----
    This function computes a discrete version of the Hankel transform

    .. math::

        a(r) = \int_{0}^{\infty} \! A(k) \, J_\mu(kr) \, r \, dk \;,

    where :math:`J_\mu` is the Bessel function of order :math:`\mu`.  The index
    :math:`\mu` may be any real number, positive or negative. Note that the
    numerical inverse Hankel transform uses an integrand of :math:`r \, dk`, while the
    mathematical inverse Hankel transform is commonly defined using :math:`k \, dk`.

    See `fht` for further details.
    """
    return (Dispatchable(A, np.ndarray),)


def ifht(A, dln, mu, offset=0.0, bias=0.0):
    xp = array_namespace(A)
    A = xp.asarray(A)

    # size of transform
    n = A.shape[-1]

    # bias input array
    if bias != 0:
        # A_q(k) = A(k) (k/k_c)^{q} (k_c r_c)^{q}
        j_c = (n-1)/2
        j = xp.arange(n, dtype=xp.float64)
        A = A * xp.exp(bias*((j - j_c)*dln + offset))

    # compute FHT coefficients
    u = xp.asarray(fhtcoeff(n, dln, mu, offset=offset, bias=bias, inverse=True))

    # transform
    a = _fhtq(A, u, inverse=True, xp=xp)

    # bias output array
    if bias != 0:
        # a(r) = a_q(r) (r/r_c)^{q}
        a /= xp.exp(-bias*(j - j_c)*dln)

    return a

