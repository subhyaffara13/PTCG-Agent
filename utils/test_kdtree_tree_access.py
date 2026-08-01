
def test_kdtree_tree_access():
    # Test KDTree.tree can be used to traverse the KDTree
    np.random.seed(1234)
    points = np.random.rand(100, 4)
    t = KDTree(points)
    visit_tree(0, t, points)

