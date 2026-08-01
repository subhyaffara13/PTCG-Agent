
def test_distance_matrix():
    m = 10
    n = 11
    k = 4
    np.random.seed(1234)
    xs = np.random.randn(m, k)
    ys = np.random.randn(n, k)
    with pytest.deprecated_call(match="1.20.0"):
        ds = distance_matrix(xs, ys)
    assert_equal(ds.shape, (m, n))
    for i in range(m):
        for j in range(n):
            with pytest.deprecated_call(match="1.20.0"):
                assert_almost_equal(minkowski_distance(xs[i], ys[j]), ds[i, j])

