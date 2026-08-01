
def test_distance_matrix_looping():
    m = 10
    n = 11
    k = 4
    np.random.seed(1234)
    xs = np.random.randn(m, k)
    ys = np.random.randn(n, k)
    with pytest.deprecated_call(match="1.20.0"):
        ds = distance_matrix(xs, ys)
    with pytest.deprecated_call(match="1.20.0"):
        dsl = distance_matrix(xs, ys, threshold=1)
    assert_equal(ds, dsl)

