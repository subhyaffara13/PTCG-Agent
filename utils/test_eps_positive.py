
def test_eps_positive():
    # np.finfo('g').eps should be positive on all platforms. If this isn't true
    # then something may have gone wrong with the MachArLike, e.g. if
    # np._core.getlimits._discovered_machar didn't work properly
    assert np.finfo(np.longdouble).eps > 0.

