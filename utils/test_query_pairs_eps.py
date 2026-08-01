
def test_query_pairs_eps(kdtree_type):
    spacing = np.sqrt(2)
    # irrational spacing to have potential rounding errors
    x_range = np.linspace(0, 3 * spacing, 4)
    y_range = np.linspace(0, 3 * spacing, 4)
    xy_array = [(xi, yi) for xi in x_range for yi in y_range]
    tree = kdtree_type(xy_array)
    pairs_eps = tree.query_pairs(r=spacing, eps=.1)
    # result: 24 with eps, 16 without due to rounding
    pairs = tree.query_pairs(r=spacing * 1.01)
    # result: 24
    assert_equal(pairs, pairs_eps)

