
def test_laplacian(graphs):
    A_dense, A_sparse = graphs
    sparse_cls = type(A_sparse)
    func = spgraph.laplacian

    actual = func(A_sparse)
    desired = func(sp.csc_array(A_dense))

    assert isinstance(actual, sparse_cls)

    assert_equal(actual.todense(), desired.todense())

