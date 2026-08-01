
def test_ckdtree_view():
    # Check that the nodes can be correctly viewed from Python.
    # This test also sanity checks each node in the cKDTree, and
    # thus verifies the internal structure of the kd-tree.
    np.random.seed(0)
    n = 100
    k = 4
    points = np.random.randn(n, k)
    kdtree = cKDTree(points)

    # walk the whole kd-tree and sanity check each node
    def recurse_tree(n):
        assert_(isinstance(n, cKDTreeNode))
        if n.split_dim == -1:
            assert_(n.lesser is None)
            assert_(n.greater is None)
            assert_(n.indices.shape[0] <= kdtree.leafsize)
        else:
            recurse_tree(n.lesser)
            recurse_tree(n.greater)
            x = n.lesser.data_points[:, n.split_dim]
            y = n.greater.data_points[:, n.split_dim]
            assert_(x.max() < y.min())

    recurse_tree(kdtree.tree)
    # check that indices are correctly retrieved
    n = kdtree.tree
    assert_array_equal(np.sort(n.indices), range(100))
    # check that data_points are correctly retrieved
    assert_array_equal(kdtree.data[n.indices, :], n.data_points)

