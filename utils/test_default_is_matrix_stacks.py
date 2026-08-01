
def test_default_is_matrix_stacks(fn):
    """Same idea as `test_default_construction_fn_matrices`, but for the
    stacking creation functions."""
    A = scipy.sparse.coo_matrix(np.eye(2))
    B = scipy.sparse.coo_matrix([[0, 1], [1, 0]])
    m = fn([A, B])
    assert not isinstance(m, scipy.sparse.sparray)

