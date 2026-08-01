
def test_TwoSlopeNorm_autoscale_None_vmin():
    norm = mcolors.TwoSlopeNorm(2, vmin=0, vmax=None)
    norm.autoscale_None([1, 2, 3, 4, 5])
    assert norm(5) == 1
    assert norm.vmax == 5

