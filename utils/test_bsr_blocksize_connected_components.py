
def test_bsr_blocksize_connected_components(graph):
    reference_graph = bsr_array(graph, blocksize=(1, 1)).astype(bool)
    sparse_graph = bsr_array(graph, blocksize=(2, 2)).astype(bool)

    n_expected, lbl_expected = csgraph.connected_components(
        reference_graph, directed=False, return_labels=True, connection="weak"
    )
    n_actual, lbl_actual = csgraph.connected_components(
        sparse_graph, directed=False, return_labels=True, connection="weak"
    )

    assert_equal(n_actual, n_expected)
    assert_allclose(lbl_actual, lbl_expected)

