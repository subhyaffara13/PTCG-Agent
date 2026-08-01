
def test_angular_rate_to_rotvec_conversions():
    np.random.seed(0)
    rv = np.random.randn(4, 3)
    A = _angular_rate_to_rotvec_dot_matrix(rv)
    A_inv = _rotvec_dot_to_angular_rate_matrix(rv)

    # When the rotation vector is aligned with the angular rate, then
    # the rotation vector rate and angular rate are the same.
    assert_allclose(_matrix_vector_product_of_stacks(A, rv), rv)
    assert_allclose(_matrix_vector_product_of_stacks(A_inv, rv), rv)

    # A and A_inv must be reciprocal to each other.
    I_stack = np.empty((4, 3, 3))
    I_stack[:] = np.eye(3)
    assert_allclose(np.matmul(A, A_inv), I_stack, atol=1e-15)

