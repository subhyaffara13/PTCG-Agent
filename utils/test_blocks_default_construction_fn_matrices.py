
def test_blocks_default_construction_fn_matrices():
    """Same idea as `test_default_construction_fn_matrices`, but block functions"""
    A = scipy.sparse.coo_matrix(np.eye(2))
    B = scipy.sparse.coo_matrix([[2], [0]])
    C = scipy.sparse.coo_matrix([[3]])

    # block diag
    m = scipy.sparse.block_diag((A, B, C))
    assert not isinstance(m, scipy.sparse.sparray)

    # bmat
    m = scipy.sparse.bmat([[A, None], [None, C]])
    assert not isinstance(m, scipy.sparse.sparray)

    # ndarray input
    A = np.eye(2)
    B = [[2], [0]]
    C = [[3]]

    # block diag
    m = scipy.sparse.block_diag((A, B, C))
    assert not isinstance(m, scipy.sparse.sparray)

    # bmat
    m = scipy.sparse.bmat([[A, None], [None, C]])
    assert not isinstance(m, scipy.sparse.sparray)

