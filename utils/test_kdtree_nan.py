
def test_kdtree_nan():
    vals = [1, 5, -10, 7, -4, -16, -6, 6, 3, -11]
    n = len(vals)
    data = np.concatenate([vals, np.full(n, np.nan)])[:, None]
    with pytest.raises(ValueError, match="must be finite"):
        KDTree(data)

