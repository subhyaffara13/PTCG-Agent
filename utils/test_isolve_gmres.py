
def test_isolve_gmres(matrices):
    # Several of the iterative solvers use the same
    # isolve.utils.make_system wrapper code, so test just one of them.
    A_dense, A_sparse, b = matrices
    x, info = splin.gmres(A_sparse, b, atol=1e-15)
    assert info == 0
    assert isinstance(x, np.ndarray)
    assert_allclose(A_sparse @ x, b)

