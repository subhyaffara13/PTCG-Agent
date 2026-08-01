
def test_matmul_equals_dot(strategy, approx_type):
    H = strategy(init_scale=1)
    H.initialize(2, approx_type)
    v = np.array([1, 2])
    assert_array_equal(H @ v, H.dot(v))

