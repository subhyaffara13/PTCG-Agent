
def test_distance_vectorization():
    np.random.seed(1234)
    x = np.random.randn(10, 1, 3)
    y = np.random.randn(1, 7, 3)
    with pytest.deprecated_call(match="1.20.0"):
        assert_equal(minkowski_distance(x, y).shape, (10, 7))

