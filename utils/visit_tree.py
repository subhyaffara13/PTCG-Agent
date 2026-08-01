
def visit_tree(i, t, points):
    root = t.tree

    assert isinstance(root, KDTree.innernode)
    assert root.children == points.shape[0]

    # Visit the tree and assert some basic properties for each node
    nodes = [root]

    while nodes:
        n = nodes.pop(-1)

        if isinstance(n, KDTree.leafnode):
            assert isinstance(n.children, int)
            assert n.children == len(n.idx)
            assert_array_equal(points[n.idx], n._node.data_points)
        else:
            assert isinstance(n, KDTree.innernode)
            assert isinstance(n.split_dim, int)
            assert 0 <= n.split_dim < t.m
            assert isinstance(n.split, float)
            assert isinstance(n.children, int)
            assert n.children == n.less.children + n.greater.children
            nodes.append(n.greater)
            nodes.append(n.less)

