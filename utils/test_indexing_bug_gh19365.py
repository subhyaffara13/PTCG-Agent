
def test_indexing_bug_gh19365():
    # Regression test for gh-19365, which reported a bug with `separate=False`
    rng = np.random.default_rng(32954827234421)
    m = rng.integers(50, high=100)
    p = rng.integers(10, 40)  # always p < m
    q = rng.integers(m - p + 1, m - 1)  # always m-p < q < m
    X = unitary_group.rvs(m, random_state=rng)  # random unitary matrix
    U, D, Vt = linalg.cossin(X, p=p, q=q, separate=False)
    assert np.allclose(U @ D @ Vt, X)

