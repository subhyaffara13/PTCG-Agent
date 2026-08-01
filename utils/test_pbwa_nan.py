
def test_pbwa_nan():
    # Check that NaN's are returned outside of the range in which the
    # implementation is accurate.
    pts = [(-6, -6), (-6, 6), (6, -6), (6, 6)]
    for p in pts:
        assert_equal(sc.pbwa(*p), (np.nan, np.nan))

