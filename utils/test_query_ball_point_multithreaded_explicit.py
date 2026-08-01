
def test_query_ball_point_multithreaded_explicit(kdtree_type):
    rng = np.random.RandomState(3819232613)
    n = 10000
    k = 2

    points = rng.randn(n, k)
    tree = kdtree_type(points)
    max_workers = 10
    assert(n//max_workers * max_workers == n)
    search_points = rng.randn(max_workers, n//max_workers, k)
    all_search_points = np.reshape(search_points, (n, k))
    radius = 0.3

    def worker_func(i, tree, search_points):
        return tree.query_ball_point(search_points[i], radius)

    results = _run_concurrent_barrier(
        max_workers, worker_func, tree, search_points)

    serial_results = tree.query_ball_point(all_search_points, radius)
    # the results from concurrent searching the tree should match the results
    # from searching the same set of points in one thread
    assert_array_equal(np.sort(np.concatenate(results)), np.sort(serial_results))

