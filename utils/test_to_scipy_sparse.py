
def test_to_scipy_sparse():
    if not np:
        skip("numpy not installed.")
    if not scipy:
        skip("scipy not installed.")
    else:
        sparse = scipy.sparse

    result = sparse.csr_matrix([[1, 2], [3, 4]], dtype='complex')
    assert np.linalg.norm((to_scipy_sparse(m) - result).todense()) == 0.0

