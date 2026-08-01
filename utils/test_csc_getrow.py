
def test_csc_getrow():
    N = 10
    np.random.seed(0)
    X = np.random.random((N, N))
    X[X > 0.7] = 0
    Xcsc = csc_matrix(X)

    for i in range(N):
        arr_row = X[i:i + 1, :]
        csc_row = Xcsc.getrow(i)

        assert_array_almost_equal(arr_row, csc_row.toarray())
        assert_(type(csc_row) is csr_matrix)

