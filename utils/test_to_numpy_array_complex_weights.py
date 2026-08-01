
def test_to_numpy_array_complex_weights(G, expected):
    G.add_edge(0, 1, weight=1 + 2j)
    A = nx.to_numpy_array(G, dtype=complex)
    npt.assert_array_equal(A, expected)

