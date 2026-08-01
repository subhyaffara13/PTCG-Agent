
def test_colormap_alpha_array():
    cmap = mpl.colormaps['viridis']
    vals = [-1, 0.5, 2]  # under, valid, over
    with pytest.raises(ValueError, match="alpha is array-like but"):
        cmap(vals, alpha=[1, 1, 1, 1])
    alpha = np.array([0.1, 0.2, 0.3])
    c = cmap(vals, alpha=alpha)
    assert_array_equal(c[:, -1], alpha)
    c = cmap(vals, alpha=alpha, bytes=True)
    assert_array_equal(c[:, -1], (alpha * 255).astype(np.uint8))

