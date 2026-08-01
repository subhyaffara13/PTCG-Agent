
def test_onenormest(B):
    C = spla.onenormest(B)
    npt.assert_allclose(C, np.linalg.norm(B.todense(), 1))


def test_onenormest(matrices):
    A_dense, A_sparse, b = matrices
    est0 = splin.onenormest(A_dense)
    est = splin.onenormest(A_sparse)
    assert_allclose(est, est0)

