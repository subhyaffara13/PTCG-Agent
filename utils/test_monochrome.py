
def test_monochrome():
    assert mcolors.ListedColormap(["red"]).monochrome
    assert mcolors.ListedColormap(["red"] * 5).monochrome
    assert not mcolors.ListedColormap(["red", "green"]).monochrome

