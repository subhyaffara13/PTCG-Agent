
def _cramer_solve(M, rhs, det_method="laplace"):
    """Solves system of linear equations using Cramer's rule.

    This method is relatively inefficient compared to other methods.
    However it only uses a single division, assuming a division-free determinant
    method is provided. This is helpful to minimize the chance of divide-by-zero
    cases in symbolic solutions to linear systems.

    Parameters
    ==========
    M : Matrix
        The matrix representing the left hand side of the equation.
    rhs : Matrix
        The matrix representing the right hand side of the equation.
    det_method : str or callable
        The method to use to calculate the determinant of the matrix.
        The default is ``'laplace'``.  If a callable is passed, it should take a
        single argument, the matrix, and return the determinant of the matrix.

    Returns
    =======
    x : Matrix
        The matrix that will satisfy ``Ax = B``.  Will have as many rows as
        matrix A has columns, and as many columns as matrix B.

    Examples
    ========

    >>> from sympy import Matrix
    >>> A = Matrix([[0, -6, 1], [0, -6, -1], [-5, -2, 3]])
    >>> B = Matrix([[-30, -9], [-18, -27], [-26, 46]])
    >>> x = A.cramer_solve(B)
    >>> x
    Matrix([
    [ 0, -5],
    [ 4,  3],
    [-6,  9]])

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Cramer%27s_rule#Explicit_formulas_for_small_systems

    """
    from .dense import zeros

    def entry(i, j):
        return rhs[i, sol] if j == col else M[i, j]

    if det_method == "bird":
        from .determinant import _det_bird
        det = _det_bird
    elif det_method == "laplace":
        from .determinant import _det_laplace
        det = _det_laplace
    elif isinstance(det_method, str):
        det = lambda matrix: matrix.det(method=det_method)
    else:
        det = det_method
    det_M = det(M)
    x = zeros(*rhs.shape)
    for sol in range(rhs.shape[1]):
        for col in range(rhs.shape[0]):
            x[col, sol] = det(M.__class__(*M.shape, entry)) / det_M
    return M.__class__(x)

