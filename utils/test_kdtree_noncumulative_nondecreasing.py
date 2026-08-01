
def test_kdtree_noncumulative_nondecreasing(kdtree_type):
    # check kdtree with duplicated inputs

    # it shall not divide more than 3 nodes.
    # root left (1), and right (2)
    kdtree = kdtree_type([[0]], leafsize=1)

    assert_raises(ValueError, kdtree.count_neighbors,
        kdtree, [0.1, 0], cumulative=False)

