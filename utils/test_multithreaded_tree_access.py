
def test_multithreaded_tree_access():
    # Test that lazily generating KDTree.tree works when tree generation
    # is reqested from multiple threads
    rng = np.random.RandomState(3116978525)
    points = rng.rand(100, 4)
    t = KDTree(points)
    _run_concurrent_barrier(10, visit_tree, t, points)

