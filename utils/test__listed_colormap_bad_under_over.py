
def test_ListedColormap_bad_under_over():
    cmap = mcolors.ListedColormap(["r", "g", "b"], bad="c", under="m", over="y")
    assert mcolors.same_color(cmap.get_bad(), "c")
    assert mcolors.same_color(cmap.get_under(), "m")
    assert mcolors.same_color(cmap.get_over(), "y")

