
def matrix_rep(op, basis):
    """
    Find the representation of an operator in a basis.

    Examples
    ========

    >>> from sympy.physics.secondquant import VarBosonicBasis, B, matrix_rep
    >>> b = VarBosonicBasis(5)
    >>> o = B(0)
    >>> matrix_rep(o, b)
    Matrix([
    [0, 1,       0,       0, 0],
    [0, 0, sqrt(2),       0, 0],
    [0, 0,       0, sqrt(3), 0],
    [0, 0,       0,       0, 2],
    [0, 0,       0,       0, 0]])
    """
    a = zeros(len(basis))
    for i in range(len(basis)):
        for j in range(len(basis)):
            a[i, j] = apply_operators(Dagger(basis[i])*op*basis[j])
    return a

