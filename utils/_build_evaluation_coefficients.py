
def _build_evaluation_coefficients(
    x, y, kernel, epsilon, powers, shift, scale, xp
):
    return _pythran_build_evaluation_coefficients(
        x, y, kernel, epsilon, powers, shift, scale
    )


def _build_evaluation_coefficients(
    x, y, kernel, epsilon, powers, shift, scale, xp
):
    """Construct the coefficients needed to evaluate
    the RBF.

    Parameters
    ----------
    x : (Q, N) float ndarray
        Evaluation point coordinates.
    y : (P, N) float ndarray
        Data point coordinates.
    kernel : str
        Name of the RBF.
    epsilon : float
        Shape parameter.
    powers : (R, N) int ndarray
        The exponents for each monomial in the polynomial.
    shift : (N,) float ndarray
        Shifts the polynomial domain for numerical stability.
    scale : (N,) float ndarray
        Scales the polynomial domain for numerical stability.

    Returns
    -------
    (Q, P + R) float ndarray

    """
    kernel_func = NAME_TO_FUNC[kernel]

    yeps = y*epsilon
    xeps = x*epsilon
    xhat = (x - shift)/scale

    # NB: changed w.r.t. pythran
    vec = xp.concat(
        [
            kernel_func(
                xp.linalg.vector_norm(
                    xeps[:, None, :] - yeps[None, :, :], axis=-1
                ), xp
            ),
            xp.prod(xhat[:, None, :] ** powers, axis=-1)
        ], axis=-1
    )

    return vec

