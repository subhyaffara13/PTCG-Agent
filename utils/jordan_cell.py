
def jordan_cell(eigenval, n):
    """
    Create a Jordan block:

    Examples
    ========

    >>> from sympy import jordan_cell
    >>> from sympy.abc import x
    >>> jordan_cell(x, 4)
    Matrix([
    [x, 1, 0, 0],
    [0, x, 1, 0],
    [0, 0, x, 1],
    [0, 0, 0, x]])
    """

    return Matrix.jordan_block(size=n, eigenvalue=eigenval)

