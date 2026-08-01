
def test_csr_rowslice():
    N = 10
    np.random.seed(0)
    X = np.random.random((N, N))
    X[X > 0.7] = 0
    Xcsr = csr_matrix(X)

    slices = [slice(None, None, None),
              slice(None, None, -1),
              slice(1, -2, 2),
              slice(-2, 1, -2)]

    for i in range(N):
        for sl in slices:
            _check_csr_rowslice(i, sl, X, Xcsr)

