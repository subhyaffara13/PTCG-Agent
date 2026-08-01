
def test_min_weight_full_bipartite_matching(graphs):
    A_dense, A_sparse = graphs
    func = spgraph.min_weight_full_bipartite_matching

    actual = func(A_sparse[0:2, 1:3])
    A_csc = sp.csc_array(A_dense)
    desired = func(A_csc[0:2, 1:3])
    desired1 = func(A_csc[0:2, 1:3].tocoo())

    assert_equal(actual, desired)
    assert_equal(actual, desired1)

