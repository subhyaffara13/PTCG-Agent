
def test_LinearSegmentedColormap_from_list_bad_under_over():
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "lsc", ["r", "g", "b"], bad="c", under="m", over="y")
    assert mcolors.same_color(cmap.get_bad(), "c")
    assert mcolors.same_color(cmap.get_under(), "m")
    assert mcolors.same_color(cmap.get_over(), "y")

