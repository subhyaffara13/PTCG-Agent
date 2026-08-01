
def test_format_scipy_sparse():
    if not np:
        skip("numpy not installed.")
    if not scipy:
        skip("scipy not installed.")

    for test in _tests:
        lhs = represent(test[0], basis=A, format='scipy.sparse')
        rhs = to_scipy_sparse(test[1])
        if isinstance(lhs, scipy_sparse_matrix):
            assert np.linalg.norm((lhs - rhs).todense()) == 0.0
        else:
            assert lhs == rhs

