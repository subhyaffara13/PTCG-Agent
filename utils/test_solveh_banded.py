
def test_solveh_banded():
    n = 10
    # construct positive definite matrix A
    Q = special_ortho_group(n, seed=1234).rvs()
    A = Q @ np.diag(1 + np.arange(n)) @ Q.T
    b = np.arange(n)
    ab = np.zeros((n, n))
    ab[0, :] = np.diagonal(A, 0)
    for i in range(1, n):
        ab[i, :-i] = np.diagonal(A, i)
    x, logdet, _ = _solveh_banded(ab, b, calc_logdet=True)
    assert_allclose(x, np.linalg.solve(A, b), rtol=1e-11)
    assert_allclose(logdet, np.log(np.linalg.det(A)), rtol=1e-11)

    # tridiagonal case
    x, logdet, _ = _solveh_banded(ab[:2], b, calc_logdet=True)
    A_tri = (
        np.diag(np.diag(A)) + np.diag(np.diag(A, -1), -1) + np.diag(np.diag(A, 1), 1)
    )
    assert_allclose(logdet, np.log(np.linalg.det(A_tri)), rtol=1e-11)

