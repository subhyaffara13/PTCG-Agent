
def test_scalarmappable_norm_update():
    norm = mcolors.Normalize()
    sm = matplotlib.cm.ScalarMappable(norm=norm, cmap='plasma')
    # sm doesn't have a stale attribute at first, set it to False
    sm.stale = False
    # The mappable should be stale after updating vmin/vmax
    norm.vmin = 5
    assert sm.stale
    sm.stale = False
    norm.vmax = 5
    assert sm.stale
    sm.stale = False
    norm.clip = True
    assert sm.stale
    # change to the CenteredNorm and TwoSlopeNorm to test those
    # Also make sure that updating the norm directly and with
    # set_norm both update the Norm callback
    norm = mcolors.CenteredNorm()
    sm.norm = norm
    sm.stale = False
    norm.vcenter = 1
    assert sm.stale
    norm = mcolors.TwoSlopeNorm(vcenter=0, vmin=-1, vmax=1)
    sm.set_norm(norm)
    sm.stale = False
    norm.vcenter = 1
    assert sm.stale

