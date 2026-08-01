
def test_TwoSlopeNorm_scaleout_center():
    # test the vmin never goes above vcenter
    norm = mcolors.TwoSlopeNorm(vcenter=0)
    norm([0, 1, 2, 3, 5])
    assert norm.vmin == -5
    assert norm.vmax == 5

