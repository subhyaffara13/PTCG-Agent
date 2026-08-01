
def _build_system(y, d, smoothing, kernel, epsilon, powers, xp):
    return _pythran_build_system(y, d, smoothing, kernel, epsilon, powers)


def _build_system(y, d, smoothing, kernel, epsilon, powers, xp):
    """Build the system used to solve for the RBF interpolant coefficients.

    Parameters
    ----------
    y : (P, N) float ndarray
        Data point coordinates.
    d : (P, S) float ndarray
        Data values at `y`.
    smoothing : (P,) float ndarray
        Smoothing parameter for each data point.
    kernel : str
        Name of the RBF.
    epsilon : float
        Shape parameter.
    powers : (R, N) int ndarray
        The exponents for each monomial in the polynomial.

    Returns
    -------
    lhs : (P + R, P + R) float ndarray
        Left-hand side matrix.
    rhs : (P + R, S) float ndarray
        Right-hand side matrix.
    shift : (N,) float ndarray
        Domain shift used to create the polynomial matrix.
    scale : (N,) float ndarray
        Domain scaling used to create the polynomial matrix.

    """
    s = d.shape[1]
    r = powers.shape[0]
    kernel_func = NAME_TO_FUNC[kernel]

    # Shift and scale the polynomial domain to be between -1 and 1
    mins = xp.min(y, axis=0)
    maxs = xp.max(y, axis=0)
    shift = (maxs + mins)/2
    scale = (maxs - mins)/2
    # The scale may be zero if there is a single point or all the points have
    # the same value for some dimension. Avoid division by zero by replacing
    # zeros with ones.
    scale = xp.where(scale == 0.0, 1.0, scale)

    yeps = y*epsilon
    yhat = (y - shift)/scale

    out_kernels  = kernel_matrix(yeps, kernel_func, xp)
    out_poly = polynomial_matrix(yhat, powers, xp)

    lhs = xp.concat(
        [
         xp.concat((out_kernels, out_poly), axis=1),
         xp.concat((out_poly.T, xp.zeros((r, r))), axis=1)
        ]
    , axis=0) + xp.diag(xp.concat([smoothing, xp.zeros(r)]))

    rhs = xp.concat([d, xp.zeros((r, s))], axis=0)

    return lhs, rhs, shift, scale

