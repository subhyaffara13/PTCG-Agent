
def test_kdtree_box_lower_bounds(kdtree_type):
    data = np.linspace(-1, 1, 10)
    assert_raises(ValueError, kdtree_type, data, leafsize=1, boxsize=1.0)

