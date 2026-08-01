
def test_kdtree_box_upper_bounds(kdtree_type):
    data = np.linspace(0, 2, 10).reshape(-1, 2)
    data[:, 1] += 10
    with pytest.raises(ValueError):
        kdtree_type(data, leafsize=1, boxsize=1.0)
    with pytest.raises(ValueError):
        kdtree_type(data, leafsize=1, boxsize=(0.0, 2.0))
    # skip a dimension.
    kdtree_type(data, leafsize=1, boxsize=(2.0, 0.0))

