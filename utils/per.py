
def per(matexpr):
    """ Matrix Permanent

    Examples
    ========

    >>> from sympy import MatrixSymbol, Matrix, per, ones
    >>> A = MatrixSymbol('A', 3, 3)
    >>> per(A)
    Permanent(A)
    >>> per(ones(5, 5))
    120
    >>> M = Matrix([1, 2, 5])
    >>> per(M)
    8
    """

    return Permanent(matexpr).doit()

