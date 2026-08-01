
def test_small_range_loglocator(numticks, lims, ticks):
    ll = mticker.LogLocator(numticks=numticks)
    if parse_version(np.version.version).major < 2:
        assert_allclose(ll.tick_values(*lims), ticks, rtol=2e-16)
    else:
        assert_array_equal(ll.tick_values(*lims), ticks)

