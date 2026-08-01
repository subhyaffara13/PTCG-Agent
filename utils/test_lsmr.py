
def test_lsmr(matrices):
    A_dense, A_sparse, b = matrices
    res0 = splin.lsmr(A_dense, b)
    res = splin.lsmr(A_sparse, b)
    assert_allclose(res[0], res0[0], atol=1e-3)

