
def test_TwoSlopeNorm_VminGTVcenter():
    with pytest.raises(ValueError):
        mcolors.TwoSlopeNorm(vmin=10, vcenter=0, vmax=20)

