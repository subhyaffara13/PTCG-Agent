
def test_tree_search(graphs, func):
    A_dense, A_sparse = graphs
    sparse_cls = type(A_sparse)

    actual = func(A_sparse, 0)
    desired = func(sp.csc_array(A_dense), 0)

    assert isinstance(actual, sparse_cls)

    assert_equal(actual.todense(), desired.todense())

