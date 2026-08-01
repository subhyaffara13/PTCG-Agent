
def test_BlockMatrix_Determinant():
    A, B, C, D = [MatrixSymbol(s, 3, 3) for s in 'ABCD']
    X = BlockMatrix([[A, B], [C, D]])
    from sympy.assumptions.ask import Q
    from sympy.assumptions.assume import assuming
    with assuming(Q.invertible(A)):
        assert det(X) == det(A) * det(X.schur('A'))

    assert isinstance(det(X), Expr)
    assert det(BlockMatrix([A])) == det(A)
    assert det(BlockMatrix([ZeroMatrix(n, n)])) == 0

