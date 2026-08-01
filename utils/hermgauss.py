
def hermgauss(deg):
    """
    Gauss-Hermite quadrature.

    Computes the sample points and weights for Gauss-Hermite quadrature.
    These sample points and weights will correctly integrate polynomials of
    degree :math:`2*deg - 1` or less over the interval :math:`[-\\inf, \\inf]`
    with the weight function :math:`f(x) = \\exp(-x^2)`.

    Parameters
    ----------
    deg : int
        Number of sample points and weights. It must be >= 1.

    Returns
    -------
    x : ndarray
        1-D ndarray containing the sample points.
    y : ndarray
        1-D ndarray containing the weights.

    Notes
    -----
    The results have only been tested up to degree 100, higher degrees may
    be problematic. The weights are determined by using the fact that

    .. math:: w_k = c / (H'_n(x_k) * H_{n-1}(x_k))

    where :math:`c` is a constant independent of :math:`k` and :math:`x_k`
    is the k'th root of :math:`H_n`, and then scaling the results to get
    the right value when integrating 1.

    Examples
    --------
    >>> from numpy.polynomial.hermite import hermgauss
    >>> hermgauss(2)
    (array([-0.70710678,  0.70710678]), array([0.88622693, 0.88622693]))

    """
    ideg = pu._as_int(deg, "deg")
    if ideg <= 0:
        raise ValueError("deg must be a positive integer")

    # first approximation of roots. We use the fact that the companion
    # matrix is symmetric in this case in order to obtain better zeros.
    c = np.array([0] * deg + [1], dtype=np.float64)
    m = hermcompanion(c)
    x = np.linalg.eigvalsh(m)

    # improve roots by one application of Newton
    dy = _normed_hermite_n(x, ideg)
    df = _normed_hermite_n(x, ideg - 1) * np.sqrt(2 * ideg)
    x -= dy / df

    # compute the weights. We scale the factor to avoid possible numerical
    # overflow.
    fm = _normed_hermite_n(x, ideg - 1)
    fm /= np.abs(fm).max()
    w = 1 / (fm * fm)

    # for Hermite we can also symmetrize
    w = (w + w[::-1]) / 2
    x = (x - x[::-1]) / 2

    # scale w to get the right value
    w *= np.sqrt(np.pi) / w.sum()

    return x, w

