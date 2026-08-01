
def test_MikotaPair(n):
    """Check lobpcg and eighs accuracy for the Mikota example
    already used in `benchmarks/benchmarks/sparse_linalg_lobpcg.py`.
    """
    def a(x):
        return cho_solve_banded((c, False), x)
    mik = MikotaPair(n)
    mik_k = mik.k
    mik_m = mik.m
    Ac = mik_k
    Bc = mik_m
    Ab = mik_k.tobanded()
    eigenvalues = mik.eigenvalues
    if n == 10:
        m = 3 # lobpcg calls eigh
    elif n == 20:
        m = 2
    else:
        m = 10
    ee = eigenvalues(m)
    tol = 100 * m * n * n * np.finfo(float).eps
    rng = np.random.default_rng(0)
    X = rng.normal(size=(n, m))
    c = cholesky_banded(Ab.astype(np.float32))
    el, _ = lobpcg(Ac, X, Bc, M=a, tol=1e-4,
                   maxiter=40, largest=False)
    accuracy = max(abs(ee - el) / ee)
    assert_allclose(accuracy, 0., atol=tol)
    B = LinearOperator((n, n), matvec=Bc, matmat=Bc, dtype='float64')
    A = LinearOperator((n, n), matvec=Ac, matmat=Ac, dtype='float64')
    c = cholesky_banded(Ab)
    a_l = LinearOperator((n, n), matvec=a, matmat=a, dtype='float64')
    ea, _ = eigsh(B, k=m, M=A, Minv=a_l, which='LA', tol=1e-4, maxiter=50,
                  v0 = rng.normal(size=(n, 1)))
    accuracy = max(abs(ee - np.sort(1./ea)) / ee)
    assert_allclose(accuracy, 0., atol=tol)

