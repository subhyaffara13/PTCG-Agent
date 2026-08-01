
def test_TwoSlopeNorm_scale():
    norm = mcolors.TwoSlopeNorm(2)
    assert norm.scaled() is False
    norm([1, 2, 3, 4])
    assert norm.scaled() is True

