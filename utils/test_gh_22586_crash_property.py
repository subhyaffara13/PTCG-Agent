
def test_gh_22586_crash_property(x, size, mode):
    # property-based test for median_filter resilience to hard crashing
    ndimage.median_filter(x, size=size, mode=mode)

