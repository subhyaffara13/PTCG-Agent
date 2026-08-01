
def test_logdet_difference_matrix(order, n):
    p = order
    logdet = _logdet_difference_matrix(order=p, n=n)
    D = np.diff(np.eye(n), n=p, axis=0)  # shape (n-p, n)
    assert_allclose(logdet, np.log(np.linalg.det(D @ D.T)), rtol=1e-11)
    eigvals = np.linalg.eigvals(D.T @ D)
    assert_allclose(logdet, np.sum(np.log(eigvals[eigvals > 1e-8])), rtol=1e-11)

