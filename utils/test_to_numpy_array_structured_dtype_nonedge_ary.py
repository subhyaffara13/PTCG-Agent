
def test_to_numpy_array_structured_dtype_nonedge_ary(G):
    """Similar to the scalar case, except has a different non-edge value for
    each named field."""
    G.add_edge(0, 1, weight=10)
    dtype = np.dtype([("weight", float), ("cost", float)])
    nonedges = np.array([(0, np.inf)], dtype=dtype)
    A = nx.to_numpy_array(G, dtype=dtype, weight=None, nonedge=nonedges)
    for attr in dtype.names:
        nonedge = nonedges[attr]
        expected = nx.to_numpy_array(G, dtype=float, weight=attr, nonedge=nonedge)
        npt.assert_array_equal(A[attr], expected)

