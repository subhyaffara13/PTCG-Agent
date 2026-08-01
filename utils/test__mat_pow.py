
def test_MatPow():
    from sympy.matrices.expressions import MatPow
    X = MatrixSymbol('X', 2, 2)
    Y = MatrixSymbol('Y', 2, 2)
    assert latex(MatPow(X, 2)) == 'X^{2}'
    assert latex(MatPow(X*X, 2)) == '\\left(X^{2}\\right)^{2}'
    assert latex(MatPow(X*Y, 2)) == '\\left(X Y\\right)^{2}'
    assert latex(MatPow(X + Y, 2)) == '\\left(X + Y\\right)^{2}'
    assert latex(MatPow(X + X, 2)) == '\\left(2 X\\right)^{2}'
    # Issue 20959
    Mx = MatrixSymbol('M^x', 2, 2)
    assert latex(MatPow(Mx, 2)) == r'\left(M^{x}\right)^{2}'


def test_MatPow():
    A = MatrixSymbol('A', n, n)

    AA = MatPow(A, 2)
    assert AA.exp == 2
    assert AA.base == A
    assert (A**n).exp == n

    assert A**0 == Identity(n)
    assert A**1 == A
    assert A**2 == AA
    assert A**-1 == Inverse(A)
    assert (A**-1)**-1 == A
    assert (A**2)**3 == A**6
    assert A**S.Half == sqrt(A)
    assert A**Rational(1, 3) == cbrt(A)
    raises(NonSquareMatrixError, lambda: MatrixSymbol('B', 3, 2)**2)

