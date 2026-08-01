
def test_LinearSegmentedColormap_bad_under_over():
    cdict = {
        'red': [(0., 0., 0.), (0.5, 1., 1.), (1., 1., 1.)],
        'green': [(0., 0., 0.), (0.25, 0., 0.), (0.75, 1., 1.), (1., 1., 1.)],
        'blue': [(0., 0., 0.), (0.5, 0., 0.), (1., 1., 1.)],
    }
    cmap = mcolors.LinearSegmentedColormap("lsc", cdict, bad="c", under="m", over="y")
    assert mcolors.same_color(cmap.get_bad(), "c")
    assert mcolors.same_color(cmap.get_under(), "m")
    assert mcolors.same_color(cmap.get_over(), "y")

