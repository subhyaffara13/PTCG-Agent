
def test_rayleigh_accuracy():
    # regression test for gh-4034
    p = stats.rayleigh.isf(stats.rayleigh.sf(9, 1), 1)
    assert_almost_equal(p, 9.0, decimal=15)

