
def test_lsqr(matrices):
    A_dense, A_sparse, b = matrices
    res0 = splin.lsqr(A_dense, b)
    res = splin.lsqr(A_sparse, b)
    assert_allclose(res[0], res0[0], atol=1e-5)

