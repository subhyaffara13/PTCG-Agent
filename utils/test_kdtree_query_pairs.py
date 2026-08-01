
def test_kdtree_query_pairs(kdtree_type):
    np.random.seed(0)
    n = 50
    k = 2
    r = 0.1
    r2 = r**2
    points = np.random.randn(n, k)
    T = kdtree_type(points)
    # brute force reference
    brute = set()
    for i in range(n):
        for j in range(i+1, n):
            v = points[i, :] - points[j, :]
            if np.dot(v, v) <= r2:
                brute.add((i, j))
    l0 = sorted(brute)
    # test default return type
    s = T.query_pairs(r)
    l1 = sorted(s)
    assert_array_equal(l0, l1)
    # test return type 'set'
    s = T.query_pairs(r, output_type='set')
    l1 = sorted(s)
    assert_array_equal(l0, l1)
    # test return type 'ndarray'
    s = set()
    arr = T.query_pairs(r, output_type='ndarray')
    for i in range(arr.shape[0]):
        s.add((int(arr[i, 0]), int(arr[i, 1])))
    l2 = sorted(s)
    assert_array_equal(l0, l2)

