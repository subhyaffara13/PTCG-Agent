
def test_lobpcg(matrices):
    A_dense, A_sparse, x = matrices
    X = x[:,None]

    w_dense, v_dense = splin.lobpcg(A_dense, X)
    w, v = splin.lobpcg(A_sparse, X)

    assert_allclose(w, w_dense)
    assert_allclose(v, v_dense)

