
def test_diagonal():
    m = Matrix(3, 3, range(9))
    d = m.diagonal()
    assert d == m.diagonal(0)
    assert tuple(d) == (0, 4, 8)
    assert tuple(m.diagonal(1)) == (1, 5)
    assert tuple(m.diagonal(-1)) == (3, 7)
    assert tuple(m.diagonal(2)) == (2,)
    assert type(m.diagonal()) == type(m)
    s = SparseMatrix(3, 3, {(1, 1): 1})
    assert type(s.diagonal()) == type(s)
    assert type(m) != type(s)
    raises(ValueError, lambda: m.diagonal(3))
    raises(ValueError, lambda: m.diagonal(-3))
    raises(ValueError, lambda: m.diagonal(pi))
    M = ones(2, 3)
    assert banded({i: list(M.diagonal(i))
        for i in range(1-M.rows, M.cols)}) == M


def test_diagonal():
    m = Matrix(3, 3, range(9))
    d = m.diagonal()
    assert d == m.diagonal(0)
    assert tuple(d) == (0, 4, 8)
    assert tuple(m.diagonal(1)) == (1, 5)
    assert tuple(m.diagonal(-1)) == (3, 7)
    assert tuple(m.diagonal(2)) == (2,)
    assert type(m.diagonal()) == type(m)
    s = SparseMatrix(3, 3, {(1, 1): 1})
    assert type(s.diagonal()) == type(s)
    assert type(m) != type(s)
    raises(ValueError, lambda: m.diagonal(3))
    raises(ValueError, lambda: m.diagonal(-3))
    raises(ValueError, lambda: m.diagonal(pi))
    M = ones(2, 3)
    assert banded({i: list(M.diagonal(i))
        for i in range(1-M.rows, M.cols)}) == M


def test_diagonal():
    assert ask(Q.diagonal(X + Z.T + Identity(2)), Q.diagonal(X) &
               Q.diagonal(Z)) is True
    assert ask(Q.diagonal(ZeroMatrix(3, 3)))
    assert ask(Q.diagonal(OneMatrix(1, 1))) is True
    assert ask(Q.diagonal(OneMatrix(3, 3))) is False
    assert ask(Q.lower_triangular(X) & Q.upper_triangular(X), Q.diagonal(X))
    assert ask(Q.diagonal(X), Q.lower_triangular(X) & Q.upper_triangular(X))
    assert ask(Q.symmetric(X), Q.diagonal(X))
    assert ask(Q.triangular(X), Q.diagonal(X))
    assert ask(Q.diagonal(C0x0))
    assert ask(Q.diagonal(A1x1))
    assert ask(Q.diagonal(A1x1 + B1x1))
    assert ask(Q.diagonal(A1x1*B1x1))
    assert ask(Q.diagonal(V1.T*V2))
    assert ask(Q.diagonal(V1.T*(X + Z)*V1))
    assert ask(Q.diagonal(MatrixSlice(Y, (0, 1), (1, 2)))) is True
    assert ask(Q.diagonal(V1.T*(V1 + V2))) is True
    assert ask(Q.diagonal(X**3), Q.diagonal(X))
    assert ask(Q.diagonal(Identity(3)))
    assert ask(Q.diagonal(DiagMatrix(V1)))
    assert ask(Q.diagonal(DiagonalMatrix(X)))


def test_diagonal(n, m, m_excluded):
    """Test ``m - m_excluded`` eigenvalues and eigenvectors of
    diagonal matrices of the size ``n`` varying matrix formats:
    dense array, spare matrix, and ``LinearOperator`` for both
    matrixes in the generalized eigenvalue problem ``Av = cBv``
    and for the preconditioner.
    """
    rnd = np.random.RandomState(0)

    # Define the generalized eigenvalue problem Av = cBv
    # where (c, v) is a generalized eigenpair,
    # A is the diagonal matrix whose entries are 1,...n,
    # B is the identity matrix.
    vals = np.arange(1, n+1, dtype=float)
    A_s = dia_array(([vals], [0]), shape=(n, n))
    A_a = A_s.toarray()

    def A_f(x):
        return A_s @ x

    A_lo = LinearOperator(matvec=A_f,
                          matmat=A_f,
                          shape=(n, n), dtype=float)

    B_a = eye_array(n)
    B_s = csr_array(B_a)

    def B_f(x):
        return B_a @ x

    B_lo = LinearOperator(matvec=B_f,
                          matmat=B_f,
                          shape=(n, n), dtype=float)

    # Let the preconditioner M be the inverse of A.
    M_s = dia_array(([1./vals], [0]), shape=(n, n))
    M_a = M_s.toarray()

    def M_f(x):
        return M_s @ x

    M_lo = LinearOperator(matvec=M_f,
                          matmat=M_f,
                          shape=(n, n), dtype=float)

    # Pick random initial vectors.
    X = rnd.normal(size=(n, m))

    # Require that the returned eigenvectors be in the orthogonal complement
    # of the first few standard basis vectors.
    if m_excluded > 0:
        Y = np.eye(n, m_excluded)
    else:
        Y = None

    for A in [A_a, A_s, A_lo]:
        for B in [B_a, B_s, B_lo]:
            for M in [M_a, M_s, M_lo]:
                eigvals, vecs = lobpcg(A, X, B, M=M, Y=Y,
                                       maxiter=40, largest=False)

                assert_allclose(eigvals, np.arange(1+m_excluded,
                                                   1+m_excluded+m))
                _check_eigen(A, eigvals, vecs, rtol=1e-3, atol=1e-3)


def test_diagonal():
    b1 = np.matrix([[1, 2], [3, 4]])
    diag_b1 = np.matrix([[1, 4]])
    array_b1 = np.array([1, 4])

    assert_equal(b1.diagonal(), diag_b1)
    assert_equal(np.diagonal(b1), array_b1)
    assert_equal(np.diag(b1), array_b1)


def test_diagonal():
    # Here we only test if selected axes are compatible
    # with Array API (last two). Core implementation
    # of `diagonal` is tested in `test_multiarray.py`.
    x = np.arange(60).reshape((3, 4, 5))
    actual = np.linalg.diagonal(x)
    expected = np.array(
        [
            [0,  6, 12, 18],
            [20, 26, 32, 38],
            [40, 46, 52, 58],
        ]
    )
    assert_equal(actual, expected)

