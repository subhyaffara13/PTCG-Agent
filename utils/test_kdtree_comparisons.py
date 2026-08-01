
def test_kdtree_comparisons():
    # Regression test: node comparisons were done wrong in 0.12 w/Py3.
    nodes = [KDTree.node() for _ in range(3)]
    assert_equal(sorted(nodes), sorted(nodes[::-1]))

