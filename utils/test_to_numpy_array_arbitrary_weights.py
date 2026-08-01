
def test_to_numpy_array_arbitrary_weights():
    G = nx.DiGraph()
    w = 922337203685477580102  # Out of range for int64
    G.add_edge(0, 1, weight=922337203685477580102)  # val not representable by int64
    A = nx.to_numpy_array(G, dtype=object)
    expected = np.array([[0, w], [0, 0]], dtype=object)
    npt.assert_array_equal(A, expected)

    # Undirected
    A = nx.to_numpy_array(G.to_undirected(), dtype=object)
    expected = np.array([[0, w], [w, 0]], dtype=object)
    npt.assert_array_equal(A, expected)

