
def test_csgraph_equiv(func, graphs):
    A_dense, A_sparse = graphs
    actual = func(A_sparse)
    desired = func(sp.csc_array(A_dense))
    assert_equal(actual, desired)

