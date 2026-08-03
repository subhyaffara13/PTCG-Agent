import itertools

def test_kdtree_duplicated_inputs(kdtree_type):
    # check kdtree with duplicated inputs
    n = 1024
    for m in range(1, 8):
        data = np.ones((n, m))
        data[n//2:] = 2

        for balanced, compact in itertools.product((False, True), repeat=2):
            kdtree = kdtree_type(data, balanced_tree=balanced,
                                 compact_nodes=compact, leafsize=1)
            assert kdtree.size == 3

            tree = (kdtree.tree if kdtree_type is cKDTree else
                    kdtree.tree._node)

            assert_equal(
                np.sort(tree.lesser.indices),
                np.arange(0, n // 2))
            assert_equal(
                np.sort(tree.greater.indices),
                np.arange(n // 2, n))

