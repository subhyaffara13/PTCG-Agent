import itertools

def test_diagonal_data_types(n, m):
    """Check lobpcg for diagonal matrices for all matrix types.
    Constraints are imposed, so a dense eigensolver eig cannot run.
    """
    rnd = np.random.RandomState(0)
    # Define the generalized eigenvalue problem Av = cBv
    # where (c, v) is a generalized eigenpair,
    # and where we choose A  and B to be diagonal.
    vals = np.arange(1, n + 1)

    list_sparse_format = ['bsr', 'coo', 'csc', 'csr', 'dia', 'dok', 'lil']
    for s_f_i, s_f in enumerate(list_sparse_format):

        As64 = dia_array(([vals * vals], [0]), shape=(n, n)).asformat(s_f)
        As32 = As64.astype(np.float32)
        Af64 = As64.toarray()
        Af32 = Af64.astype(np.float32)

        def As32f(x):
            return As32 @ x
        As32LO = LinearOperator(matvec=As32f,
                                matmat=As32f,
                                shape=(n, n),
                                dtype=As32.dtype)

        listA = [Af64, As64, Af32, As32, As32f, As32LO, lambda v: As32 @ v]

        Bs64 = dia_array(([vals], [0]), shape=(n, n)).asformat(s_f)
        Bf64 = Bs64.toarray()
        Bs32 = Bs64.astype(np.float32)

        def Bs32f(x):
            return Bs32 @ x
        Bs32LO = LinearOperator(matvec=Bs32f,
                                matmat=Bs32f,
                                shape=(n, n),
                                dtype=Bs32.dtype)
        listB = [Bf64, Bs64, Bs32, Bs32f, Bs32LO, lambda v: Bs32 @ v]

        # Define the preconditioner function as LinearOperator.
        Ms64 = dia_array(([1./vals], [0]), shape=(n, n)).asformat(s_f)

        def Ms64precond(x):
            return Ms64 @ x
        Ms64precondLO = LinearOperator(matvec=Ms64precond,
                                       matmat=Ms64precond,
                                       shape=(n, n),
                                       dtype=Ms64.dtype)
        Mf64 = Ms64.toarray()

        def Mf64precond(x):
            return Mf64 @ x
        Mf64precondLO = LinearOperator(matvec=Mf64precond,
                                       matmat=Mf64precond,
                                       shape=(n, n),
                                       dtype=Mf64.dtype)
        Ms32 = Ms64.astype(np.float32)

        def Ms32precond(x):
            return Ms32 @ x
        Ms32precondLO = LinearOperator(matvec=Ms32precond,
                                       matmat=Ms32precond,
                                       shape=(n, n),
                                       dtype=Ms32.dtype)
        Mf32 = Ms32.toarray()

        def Mf32precond(x):
            return Mf32 @ x
        Mf32precondLO = LinearOperator(matvec=Mf32precond,
                                       matmat=Mf32precond,
                                       shape=(n, n),
                                       dtype=Mf32.dtype)
        listM = [None, Ms64, Ms64precondLO, Mf64precondLO, Ms64precond,
                 Ms32, Ms32precondLO, Mf32precondLO, Ms32precond]

        # Setup matrix of the initial approximation to the eigenvectors
        # (cannot be sparse array).
        Xf64 = rnd.random((n, m))
        Xf32 = Xf64.astype(np.float32)
        listX = [Xf64, Xf32]

        # Require that the returned eigenvectors be in the orthogonal complement
        # of the first few standard basis vectors (cannot be sparse array).
        m_excluded = 3
        Yf64 = np.eye(n, m_excluded, dtype=float)
        Yf32 = np.eye(n, m_excluded, dtype=np.float32)
        listY = [Yf64, Yf32]

        tests = list(itertools.product(listA, listB, listM, listX, listY))

        for A, B, M, X, Y in tests:
            # This is one of the slower tests because there are >1,000 configs
            # to test here. Flip a biased coin to decide whether to run  each
            # test to get decent coverage in less time.
            if rnd.random() < 0.98:
                continue  # too many tests
            eigvals, _ = lobpcg(A, X, B=B, M=M, Y=Y, tol=1e-4,
                                maxiter=100, largest=False)
            assert_allclose(eigvals,
                            np.arange(1 + m_excluded, 1 + m_excluded + m),
                            atol=1e-5)

