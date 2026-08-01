
def test_return_type(method):
    graph = csr_array([[0, 5], [0, 0]])
    assert isinstance(maximum_flow(graph, 0, 1, method=method).flow, csr_array)
    graph = csr_matrix([[0, 5], [0, 0]])
    assert isinstance(maximum_flow(graph, 0, 1, method=method).flow, csr_matrix)


def test_return_type():
    from .._laplacian import laplacian
    from .._min_spanning_tree import minimum_spanning_tree

    np_csgraph = np.array([[0, 1, 2, 0, 0],
                           [1, 0, 0, 0, 3],
                           [2, 0, 0, 7, 0],
                           [0, 0, 7, 0, 1],
                           [0, 3, 0, 1, 0]])
    csgraph = csr_array(np_csgraph)
    assert isinstance(laplacian(csgraph), coo_array)
    assert isinstance(minimum_spanning_tree(csgraph), csr_array)
    for directed in [True, False]:
        assert isinstance(depth_first_tree(csgraph, 0, directed), csr_array)
        assert isinstance(breadth_first_tree(csgraph, 0, directed), csr_array)

    csgraph = csgraph_from_dense(np_csgraph, null_value=0)
    assert isinstance(csgraph, csr_array)
    assert isinstance(laplacian(csgraph), coo_array)
    assert isinstance(minimum_spanning_tree(csgraph), csr_array)
    for directed in [True, False]:
        assert isinstance(depth_first_tree(csgraph, 0, directed), csr_array)
        assert isinstance(breadth_first_tree(csgraph, 0, directed), csr_array)

    csgraph = csgraph_masked_from_dense(np_csgraph, null_value=0)
    assert isinstance(csgraph, np.ma.MaskedArray)
    assert csgraph._baseclass is np.ndarray
    # laplacian doesnt work with masked arrays so not here
    assert isinstance(minimum_spanning_tree(csgraph), csr_array)
    for directed in [True, False]:
        assert isinstance(depth_first_tree(csgraph, 0, directed), csr_array)
        assert isinstance(breadth_first_tree(csgraph, 0, directed), csr_array)

    # start of testing with matrix/spmatrix types
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "the matrix subclass.*", DeprecationWarning)
        warnings.filterwarnings(
            "ignore", "the matrix subclass.*", PendingDeprecationWarning)

        nm_csgraph = np.matrix([[0, 1, 2, 0, 0],
                                [1, 0, 0, 0, 3],
                                [2, 0, 0, 7, 0],
                                [0, 0, 7, 0, 1],
                                [0, 3, 0, 1, 0]])

    csgraph = csr_matrix(nm_csgraph)
    assert isinstance(laplacian(csgraph), coo_matrix)
    assert isinstance(minimum_spanning_tree(csgraph), csr_matrix)
    for directed in [True, False]:
        assert isinstance(depth_first_tree(csgraph, 0, directed), csr_matrix)
        assert isinstance(breadth_first_tree(csgraph, 0, directed), csr_matrix)

    csgraph = csgraph_from_dense(nm_csgraph, null_value=0)
    assert isinstance(csgraph, csr_matrix)
    assert isinstance(laplacian(csgraph), coo_matrix)
    assert isinstance(minimum_spanning_tree(csgraph), csr_matrix)
    for directed in [True, False]:
        assert isinstance(depth_first_tree(csgraph, 0, directed), csr_matrix)
        assert isinstance(breadth_first_tree(csgraph, 0, directed), csr_matrix)

    mm_csgraph = csgraph_masked_from_dense(nm_csgraph, null_value=0)
    assert isinstance(mm_csgraph, np.ma.MaskedArray)
    # laplacian doesnt work with masked arrays so not here
    assert isinstance(minimum_spanning_tree(csgraph), csr_matrix)
    for directed in [True, False]:
        assert isinstance(depth_first_tree(csgraph, 0, directed), csr_matrix)
        assert isinstance(breadth_first_tree(csgraph, 0, directed), csr_matrix)

