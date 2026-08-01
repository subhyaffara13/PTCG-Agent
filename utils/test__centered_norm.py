
def test_CenteredNorm():
    np.random.seed(0)

    # Assert equivalence to symmetrical Normalize.
    x = np.random.normal(size=100)
    x_maxabs = np.max(np.abs(x))
    norm_ref = mcolors.Normalize(vmin=-x_maxabs, vmax=x_maxabs)
    norm = mcolors.CenteredNorm()
    assert_array_almost_equal(norm_ref(x), norm(x))

    # Check that vcenter is in the center of vmin and vmax
    # when vcenter is set.
    vcenter = int(np.random.normal(scale=50))
    norm = mcolors.CenteredNorm(vcenter=vcenter)
    norm.autoscale_None([1, 2])
    assert norm.vmax + norm.vmin == 2 * vcenter

    # Check that halfrange can be set without setting vcenter and that it is
    # not reset through autoscale_None.
    norm = mcolors.CenteredNorm(halfrange=1.0)
    norm.autoscale_None([1, 3000])
    assert norm.halfrange == 1.0

    # Check that halfrange input works correctly.
    x = np.random.normal(size=10)
    norm = mcolors.CenteredNorm(vcenter=0.5, halfrange=0.5)
    assert_array_almost_equal(x, norm(x))
    norm = mcolors.CenteredNorm(vcenter=1, halfrange=1)
    assert_array_almost_equal(x, 2 * norm(x))

    # Check that halfrange input works correctly and use setters.
    norm = mcolors.CenteredNorm()
    norm.vcenter = 2
    norm.halfrange = 2
    assert_array_almost_equal(x, 4 * norm(x))

    # Check that prior to adding data, setting halfrange first has same effect.
    norm = mcolors.CenteredNorm()
    norm.halfrange = 2
    norm.vcenter = 2
    assert_array_almost_equal(x, 4 * norm(x))

    # Check that manual change of vcenter adjusts halfrange accordingly.
    norm = mcolors.CenteredNorm()
    assert norm.vcenter == 0
    # add data
    norm(np.linspace(-1.0, 0.0, 10))
    assert norm.vmax == 1.0
    assert norm.halfrange == 1.0
    # set vcenter to 1, which should move the center but leave the
    # halfrange unchanged
    norm.vcenter = 1
    assert norm.vmin == 0
    assert norm.vmax == 2
    assert norm.halfrange == 1

    # Check setting vmin directly updates the halfrange and vmax, but
    # leaves vcenter alone
    norm.vmin = -1
    assert norm.halfrange == 2
    assert norm.vmax == 3
    assert norm.vcenter == 1

    # also check vmax updates
    norm.vmax = 2
    assert norm.halfrange == 1
    assert norm.vmin == 0
    assert norm.vcenter == 1

