
def test_maximum_flow(graphs):
    A_dense, A_sparse = graphs
    sparse_cls = type(A_sparse)
    func = spgraph.maximum_flow

    actual = func(A_sparse, 0, 2)
    desired = func(sp.csr_array(A_dense), 0, 2)

    assert actual.flow_value == desired.flow_value
    assert isinstance(actual.flow, sparse_cls)

    assert_equal(actual.flow.todense(), desired.flow.todense())

