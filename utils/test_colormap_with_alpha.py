
def test_colormap_with_alpha():
    cmap = ListedColormap(["red", "green", ("blue", 0.8)])
    cmap2 = cmap.with_alpha(0.5)
    # color is the same:
    vals = [0, 0.5, 1]  # numeric positions that map to the listed colors
    assert_array_equal(cmap(vals)[:, :3], cmap2(vals)[:, :3])
    # alpha of cmap2 is changed:
    assert_array_equal(cmap(vals)[:, 3], [1, 1, 0.8])
    assert_array_equal(cmap2(vals)[:, 3], [0.5, 0.5, 0.5])

