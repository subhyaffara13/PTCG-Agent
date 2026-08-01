
def test_fully_connected_graph():
    # Fully connected dense matrices raised an exception.
    # https://github.com/scipy/scipy/issues/3818
    g = np.ones((4, 4))
    n_components, labels = csgraph.connected_components(g)
    assert_equal(n_components, 1)

