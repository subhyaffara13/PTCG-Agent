
def test_TwoSlopeNorm_VcenterGTVmax():
    with pytest.raises(ValueError):
        mcolors.TwoSlopeNorm(vmin=10, vcenter=25, vmax=20)

