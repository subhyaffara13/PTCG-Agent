import re

def test_ZeroMatrix():
    from sympy.matrices.expressions.special import ZeroMatrix
    assert latex(ZeroMatrix(1, 1), mat_symbol_style='plain') == r"0"
    assert latex(ZeroMatrix(1, 1), mat_symbol_style='bold') == r"\mathbf{0}"


def test_ZeroMatrix():
    n, m = symbols('n m', integer=True)
    A = MatrixSymbol('A', n, m)
    Z = ZeroMatrix(n, m)

    assert A + Z == A
    assert A*Z.T == ZeroMatrix(n, n)
    assert Z*A.T == ZeroMatrix(n, n)
    assert A - A == ZeroMatrix(*A.shape)

    assert Z

    assert Z.transpose() == ZeroMatrix(m, n)
    assert Z.conjugate() == Z
    assert Z.adjoint() == ZeroMatrix(m, n)
    assert re(Z) == Z
    assert im(Z) == Z

    assert ZeroMatrix(n, n)**0 == Identity(n)
    assert ZeroMatrix(3, 3).as_explicit() == ImmutableDenseMatrix.zeros(3, 3)

