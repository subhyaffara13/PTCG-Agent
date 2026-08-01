
def test_query_pairs_single_node(kdtree_type):
    tree = kdtree_type([[0, 1]])
    assert_equal(tree.query_pairs(0.5), set())

