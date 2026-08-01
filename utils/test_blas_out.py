
def test_blas_out() -> None:
    np = pytest.importorskip("numpy")

    a = np.random.rand(4, 4)
    b = np.random.rand(4, 4)
    c = np.random.rand(4, 4)
    d = np.empty((4, 4))

    contract("ij,jk->ik", a, b, out=d)
    np.testing.assert_allclose(d, np.dot(a, b))
    assert np.allclose(d, np.dot(a, b))

    contract("ij,jk,kl->il", a, b, c, out=d)
    np.testing.assert_allclose(d, np.dot(a, b).dot(c))

