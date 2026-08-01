
def test_norm_deepcopy():
    norm = mcolors.LogNorm()
    norm.vmin = 0.0002
    norm2 = copy.deepcopy(norm)
    assert norm2.vmin == norm.vmin
    assert isinstance(norm2._scale, mscale.LogScale)
    norm = mcolors.Normalize()
    norm.vmin = 0.0002
    norm2 = copy.deepcopy(norm)
    assert norm2._scale is None
    assert norm2.vmin == norm.vmin

