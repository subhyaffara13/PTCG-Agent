
def solve_linear_system_LU(matrix, syms):
    """
    Solves the augmented matrix system using ``LUsolve`` and returns a
    dictionary in which solutions are keyed to the symbols of *syms* as ordered.

    Explanation
    ===========

    The matrix must be invertible.

    Examples
    ========

    >>> from sympy import Matrix, solve_linear_system_LU
    >>> from sympy.abc import x, y, z

    >>> solve_linear_system_LU(Matrix([
    ... [1, 2, 0, 1],
    ... [3, 2, 2, 1],
    ... [2, 0, 0, 1]]), [x, y, z])
    {x: 1/2, y: 1/4, z: -1/2}

    See Also
    ========

    LUsolve

    """
    if matrix.rows != matrix.cols - 1:
        raise ValueError("Rows should be equal to columns - 1")
    A = matrix[:matrix.rows, :matrix.rows]
    b = matrix[:, matrix.cols - 1:]
    soln = A.LUsolve(b)
    solutions = {}
    for i in range(soln.rows):
        solutions[syms[i]] = soln[i, 0]
    return solutions

