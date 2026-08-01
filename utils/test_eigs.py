
def test_eigs(X):
    e, v = spla.eigs(X, k=1)
    npt.assert_allclose(
        X @ v,
        e[0] * v
    )


def test_eigs(matrices):
    A_dense, A_sparse, v0 = matrices

    M_dense = np.diag(v0**2)
    M_sparse = A_sparse.__class__(M_dense)

    w_dense, v_dense = splin.eigs(A_dense, k=3, v0=v0)
    w, v = splin.eigs(A_sparse, k=3, v0=v0)

    assert_allclose(w, w_dense)
    assert_allclose(v, v_dense)

    for M in [M_sparse, M_dense]:
        w_dense, v_dense = splin.eigs(A_dense, M=M_dense, k=3, v0=v0)
        w, v = splin.eigs(A_sparse, M=M, k=3, v0=v0)

        assert_allclose(w, w_dense)
        assert_allclose(v, v_dense)

        w_dense, v_dense = splin.eigsh(A_dense, M=M_dense, k=3, v0=v0)
        w, v = splin.eigsh(A_sparse, M=M, k=3, v0=v0)

        assert_allclose(w, w_dense)
        assert_allclose(v, v_dense)

