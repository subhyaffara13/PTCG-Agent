
def test_multiple_edges():
    # create a random square matrix with an even number of elements
    np.random.seed(1234)
    X = np.random.random((10, 10))
    Xcsr = csr_array(X)

    # now double-up every other column
    Xcsr.indices[::2] = Xcsr.indices[1::2]

    # normal sparse toarray() will sum the duplicated edges
    Xdense = Xcsr.toarray()
    assert_array_almost_equal(Xdense[:, 1::2],
                              X[:, ::2] + X[:, 1::2])

    # csgraph_to_dense chooses the minimum of each duplicated edge
    Xdense = csgraph_to_dense(Xcsr)
    assert_array_almost_equal(Xdense[:, 1::2],
                              np.minimum(X[:, ::2], X[:, 1::2]))

