
def test_TwoSlopeNorm_TwoSlopeNorm_VminGTVmax():
    with pytest.raises(ValueError):
        mcolors.TwoSlopeNorm(vmin=10, vcenter=0, vmax=5)

