
def test_eigsh(X):
    X = X + X.T
    e, v = spla.eigsh(X, k=1)
    npt.assert_allclose(
        X @ v,
        e[0] * v
    )

