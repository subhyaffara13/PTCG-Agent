
def test_LDLdecomposition():
    raises(NonSquareMatrixError, lambda: Matrix((1, 2)).LDLdecomposition())
    raises(ValueError, lambda: Matrix(((1, 2), (3, 4))).LDLdecomposition())
    raises(ValueError, lambda: Matrix(((5 + I, 0), (0, 1))).LDLdecomposition())
    raises(ValueError, lambda: Matrix(((1, 5), (5, 1))).LDLdecomposition())
    raises(ValueError, lambda: Matrix(((1, 2), (3, 4))).LDLdecomposition(hermitian=False))
    A = Matrix(((1, 5), (5, 1)))
    L, D = A.LDLdecomposition(hermitian=False)
    assert L * D * L.T == A
    A = Matrix(((25, 15, -5), (15, 18, 0), (-5, 0, 11)))
    L, D = A.LDLdecomposition()
    assert L * D * L.T == A
    assert L.is_lower
    assert L == Matrix([[1, 0, 0], [ Rational(3, 5), 1, 0], [Rational(-1, 5), Rational(1, 3), 1]])
    assert D.is_diagonal()
    assert D == Matrix([[25, 0, 0], [0, 9, 0], [0, 0, 9]])
    A = Matrix(((4, -2*I, 2 + 2*I), (2*I, 2, -1 + I), (2 - 2*I, -1 - I, 11)))
    L, D = A.LDLdecomposition()
    assert expand_mul(L * D * L.H) == A
    assert L.expand() == Matrix([[1, 0, 0], [I/2, 1, 0], [S.Half - I/2, 0, 1]])
    assert D.expand() == Matrix(((4, 0, 0), (0, 1, 0), (0, 0, 9)))

    raises(NonSquareMatrixError, lambda: SparseMatrix((1, 2)).LDLdecomposition())
    raises(ValueError, lambda: SparseMatrix(((1, 2), (3, 4))).LDLdecomposition())
    raises(ValueError, lambda: SparseMatrix(((5 + I, 0), (0, 1))).LDLdecomposition())
    raises(ValueError, lambda: SparseMatrix(((1, 5), (5, 1))).LDLdecomposition())
    raises(ValueError, lambda: SparseMatrix(((1, 2), (3, 4))).LDLdecomposition(hermitian=False))
    A = SparseMatrix(((1, 5), (5, 1)))
    L, D = A.LDLdecomposition(hermitian=False)
    assert L * D * L.T == A
    A = SparseMatrix(((25, 15, -5), (15, 18, 0), (-5, 0, 11)))
    L, D = A.LDLdecomposition()
    assert L * D * L.T == A
    assert L.is_lower
    assert L == Matrix([[1, 0, 0], [ Rational(3, 5), 1, 0], [Rational(-1, 5), Rational(1, 3), 1]])
    assert D.is_diagonal()
    assert D == Matrix([[25, 0, 0], [0, 9, 0], [0, 0, 9]])
    A = SparseMatrix(((4, -2*I, 2 + 2*I), (2*I, 2, -1 + I), (2 - 2*I, -1 - I, 11)))
    L, D = A.LDLdecomposition()
    assert expand_mul(L * D * L.H) == A
    assert L == Matrix(((1, 0, 0), (I/2, 1, 0), (S.Half - I/2, 0, 1)))
    assert D == Matrix(((4, 0, 0), (0, 1, 0), (0, 0, 9)))

