
def test_order_search(graphs, func):
    A_dense, A_sparse = graphs

    actual = func(A_sparse, 0)
    desired = func(sp.csc_array(A_dense), 0)

    assert_equal(actual, desired)

