
def test_reml_criterion(order):
    la = 1.2345
    n = 10
    y = np.sin(2*np.pi * np.linspace(0, 1, n))
    D = np.diff(np.eye(n), n=order, axis=0)
    M = D.T @ D

    def test_reml(la, y):
        # See docstring and comment of _reml.
        A = np.eye(n) + la * M
        x = np.linalg.solve(A, y)
        resid = y - x
        r2 = resid @ resid + la * x @ M @ x
        return -0.5 * ((n-order) * (1 + np.log(r2 / (n - order)))
                       - np.log(np.linalg.det(la * D @ D.T))
                       + np.log(np.linalg.det(A)))

    r1 = _reml(lamb=la, y=y, order=order)
    r2 = test_reml(la=la, y=y)
    assert_allclose(r1, r2, rtol=1e-11)

