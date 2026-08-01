
def test_from_scipy_sparse_array_formats(sparse_format):
    """Test all formats supported by _generate_weighted_edges."""
    # trinode complete graph with non-uniform edge weights
    expected = nx.Graph()
    expected.add_edges_from(
        [
            (0, 1, {"weight": 3}),
            (0, 2, {"weight": 2}),
            (1, 0, {"weight": 3}),
            (1, 2, {"weight": 1}),
            (2, 0, {"weight": 2}),
            (2, 1, {"weight": 1}),
        ]
    )
    A = sp.sparse.coo_array([[0, 3, 2], [3, 0, 1], [2, 1, 0]]).asformat(sparse_format)
    assert graphs_equal(expected, nx.from_scipy_sparse_array(A))

