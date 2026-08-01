
def test_OneMatrix():
    from sympy.matrices.expressions.special import OneMatrix
    assert latex(OneMatrix(3, 4), mat_symbol_style='plain') == r"1"
    assert latex(OneMatrix(3, 4), mat_symbol_style='bold') == r"\mathbf{1}"


def test_OneMatrix():
    n, m = symbols('n m', integer=True)
    A = MatrixSymbol('A', n, m)
    U = OneMatrix(n, m)

    assert U.shape == (n, m)
    assert isinstance(A + U, Add)
    assert U.transpose() == OneMatrix(m, n)
    assert U.conjugate() == U
    assert U.adjoint() == OneMatrix(m, n)
    assert re(U) == U
    assert im(U) == ZeroMatrix(n, m)

    assert OneMatrix(n, n) ** 0 == Identity(n)

    U = OneMatrix(n, n)
    assert U[1, 2] == 1

    U = OneMatrix(2, 3)
    assert U.as_explicit() == ImmutableDenseMatrix.ones(2, 3)

