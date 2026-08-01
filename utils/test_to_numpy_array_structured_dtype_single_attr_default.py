
def test_to_numpy_array_structured_dtype_single_attr_default():
    G = nx.path_graph(3)
    dtype = np.dtype([("weight", float)])  # A single named field
    A = nx.to_numpy_array(G, dtype=dtype, weight=None)
    expected = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=float)
    npt.assert_array_equal(A["weight"], expected)

