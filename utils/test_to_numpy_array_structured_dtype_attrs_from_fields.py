
def test_to_numpy_array_structured_dtype_attrs_from_fields(G, expected):
    """When `dtype` is structured (i.e. has names) and `weight` is None, use
    the named fields of the dtype to look up edge attributes."""
    G.add_edge(0, 1, weight=10, cost=5.0)
    dtype = np.dtype([("weight", int), ("cost", int)])
    A = nx.to_numpy_array(G, dtype=dtype, weight=None)
    expected = np.asarray(expected, dtype=dtype)
    npt.assert_array_equal(A, expected)

