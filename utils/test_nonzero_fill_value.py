
def test_nonzero_fill_value(graphs, func, fill_value, comp_func):
    A_dense, A_sparse = graphs
    A_sparse = A_sparse.astype(float)
    A_sparse.fill_value = fill_value
    sparse_cls = type(A_sparse)

    actual = func(A_sparse)
    desired = func(sp.csc_array(A_dense))

    if func == spgraph.minimum_spanning_tree:
        assert isinstance(actual, sparse_cls)
        assert comp_func(actual.fill_value)
        actual = actual.todense()
        actual[comp_func(actual)] = 0.0
        assert_equal(actual, desired.todense())
    else:
        assert_equal(actual, desired)

