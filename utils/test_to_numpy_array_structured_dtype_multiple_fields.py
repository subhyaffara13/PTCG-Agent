
def test_to_numpy_array_structured_dtype_multiple_fields(graph_type, edge):
    G = graph_type([edge])
    dtype = np.dtype([("weight", float), ("cost", float), ("flow", float)])
    A = nx.to_numpy_array(G, dtype=dtype, weight=None)
    for attr in dtype.names:
        expected = nx.to_numpy_array(G, dtype=float, weight=attr)
        npt.assert_array_equal(A[attr], expected)

