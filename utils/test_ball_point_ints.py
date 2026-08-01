
def test_ball_point_ints(kdtree_type):
    # Regression test for #1373.
    x, y = np.mgrid[0:4, 0:4]
    points = list(zip(x.ravel(), y.ravel()))
    tree = kdtree_type(points)
    assert_equal(sorted([4, 8, 9, 12]),
                 sorted(tree.query_ball_point((2, 0), 1)))
    points = np.asarray(points, dtype=float)
    tree = kdtree_type(points)
    assert_equal(sorted([4, 8, 9, 12]),
                 sorted(tree.query_ball_point((2, 0), 1)))

