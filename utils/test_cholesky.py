
def test_cholesky():
    raises(NonSquareMatrixError, lambda: Matrix((1, 2)).cholesky())
    raises(ValueError, lambda: Matrix(((1, 2), (3, 4))).cholesky())
    raises(ValueError, lambda: Matrix(((5 + I, 0), (0, 1))).cholesky())
    raises(ValueError, lambda: Matrix(((1, 5), (5, 1))).cholesky())
    raises(ValueError, lambda: Matrix(((1, 2), (3, 4))).cholesky(hermitian=False))
    assert Matrix(((5 + I, 0), (0, 1))).cholesky(hermitian=False) == Matrix([
        [sqrt(5 + I), 0], [0, 1]])
    A = Matrix(((1, 5), (5, 1)))
    L = A.cholesky(hermitian=False)
    assert L == Matrix([[1, 0], [5, 2*sqrt(6)*I]])
    assert L*L.T == A
    A = Matrix(((25, 15, -5), (15, 18, 0), (-5, 0, 11)))
    L = A.cholesky()
    assert L * L.T == A
    assert L.is_lower
    assert L == Matrix([[5, 0, 0], [3, 3, 0], [-1, 1, 3]])
    A = Matrix(((4, -2*I, 2 + 2*I), (2*I, 2, -1 + I), (2 - 2*I, -1 - I, 11)))
    assert A.cholesky().expand() == Matrix(((2, 0, 0), (I, 1, 0), (1 - I, 0, 3)))

    raises(NonSquareMatrixError, lambda: SparseMatrix((1, 2)).cholesky())
    raises(ValueError, lambda: SparseMatrix(((1, 2), (3, 4))).cholesky())
    raises(ValueError, lambda: SparseMatrix(((5 + I, 0), (0, 1))).cholesky())
    raises(ValueError, lambda: SparseMatrix(((1, 5), (5, 1))).cholesky())
    raises(ValueError, lambda: SparseMatrix(((1, 2), (3, 4))).cholesky(hermitian=False))
    assert SparseMatrix(((5 + I, 0), (0, 1))).cholesky(hermitian=False) == Matrix([
        [sqrt(5 + I), 0], [0, 1]])
    A = SparseMatrix(((1, 5), (5, 1)))
    L = A.cholesky(hermitian=False)
    assert L == Matrix([[1, 0], [5, 2*sqrt(6)*I]])
    assert L*L.T == A
    A = SparseMatrix(((25, 15, -5), (15, 18, 0), (-5, 0, 11)))
    L = A.cholesky()
    assert L * L.T == A
    assert L.is_lower
    assert L == Matrix([[5, 0, 0], [3, 3, 0], [-1, 1, 3]])
    A = SparseMatrix(((4, -2*I, 2 + 2*I), (2*I, 2, -1 + I), (2 - 2*I, -1 - I, 11)))
    assert A.cholesky() == Matrix(((2, 0, 0), (I, 1, 0), (1 - I, 0, 3)))


def test_cholesky():
    raises(NonSquareMatrixError, lambda: Matrix((1, 2)).cholesky())
    raises(ValueError, lambda: Matrix(((1, 2), (3, 4))).cholesky())
    raises(ValueError, lambda: Matrix(((5 + I, 0), (0, 1))).cholesky())
    raises(ValueError, lambda: Matrix(((1, 5), (5, 1))).cholesky())
    raises(ValueError, lambda: Matrix(((1, 2), (3, 4))).cholesky(hermitian=False))
    assert Matrix(((5 + I, 0), (0, 1))).cholesky(hermitian=False) == Matrix([
        [sqrt(5 + I), 0], [0, 1]])
    A = Matrix(((1, 5), (5, 1)))
    L = A.cholesky(hermitian=False)
    assert L == Matrix([[1, 0], [5, 2*sqrt(6)*I]])
    assert L*L.T == A
    A = Matrix(((25, 15, -5), (15, 18, 0), (-5, 0, 11)))
    L = A.cholesky()
    assert L * L.T == A
    assert L.is_lower
    assert L == Matrix([[5, 0, 0], [3, 3, 0], [-1, 1, 3]])
    A = Matrix(((4, -2*I, 2 + 2*I), (2*I, 2, -1 + I), (2 - 2*I, -1 - I, 11)))
    assert A.cholesky().expand() == Matrix(((2, 0, 0), (I, 1, 0), (1 - I, 0, 3)))

    raises(NonSquareMatrixError, lambda: SparseMatrix((1, 2)).cholesky())
    raises(ValueError, lambda: SparseMatrix(((1, 2), (3, 4))).cholesky())
    raises(ValueError, lambda: SparseMatrix(((5 + I, 0), (0, 1))).cholesky())
    raises(ValueError, lambda: SparseMatrix(((1, 5), (5, 1))).cholesky())
    raises(ValueError, lambda: SparseMatrix(((1, 2), (3, 4))).cholesky(hermitian=False))
    assert SparseMatrix(((5 + I, 0), (0, 1))).cholesky(hermitian=False) == Matrix([
        [sqrt(5 + I), 0], [0, 1]])
    A = SparseMatrix(((1, 5), (5, 1)))
    L = A.cholesky(hermitian=False)
    assert L == Matrix([[1, 0], [5, 2*sqrt(6)*I]])
    assert L*L.T == A
    A = SparseMatrix(((25, 15, -5), (15, 18, 0), (-5, 0, 11)))
    L = A.cholesky()
    assert L * L.T == A
    assert L.is_lower
    assert L == Matrix([[5, 0, 0], [3, 3, 0], [-1, 1, 3]])
    A = SparseMatrix(((4, -2*I, 2 + 2*I), (2*I, 2, -1 + I), (2 - 2*I, -1 - I, 11)))
    assert A.cholesky() == Matrix(((2, 0, 0), (I, 1, 0), (1 - I, 0, 3)))


def test_cholesky():
    assert fp.cholesky(fp.matrix(A9)) == fp.matrix([[2, 0, 0], [1, 2, 0], [-1, -3/2, 3/2]])
    x = fp.cholesky_solve(A9, b9)
    assert fp.norm(fp.residual(A9, x, b9), fp.inf) == 0

