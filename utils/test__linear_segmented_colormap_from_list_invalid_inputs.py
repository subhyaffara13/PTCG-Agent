
def test_LinearSegmentedColormap_from_list_invalid_inputs(colors):
    with pytest.raises(ValueError):
        mcolors.LinearSegmentedColormap.from_list("lsc", colors)

