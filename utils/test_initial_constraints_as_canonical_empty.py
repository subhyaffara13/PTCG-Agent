
def test_initial_constraints_as_canonical_empty():
    n = 3
    for sparse_jacobian in [False, True]:
        c_eq, c_ineq, J_eq, J_ineq = initial_constraints_as_canonical(
            n, [], sparse_jacobian)

        assert_array_equal(c_eq, [])
        assert_array_equal(c_ineq, [])

        if sparse_jacobian:
            J_eq = J_eq.toarray()
            J_ineq = J_ineq.toarray()

        assert_array_equal(J_eq, np.empty((0, n)))
        assert_array_equal(J_ineq, np.empty((0, n)))

