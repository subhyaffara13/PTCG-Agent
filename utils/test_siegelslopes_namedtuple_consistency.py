
def test_siegelslopes_namedtuple_consistency():
    """
    Simple test to ensure tuple backwards-compatibility of the returned
    SiegelslopesResult object.
    """
    y = [1, 2, 4]
    x = [4, 6, 8]
    slope, intercept = mstats.siegelslopes(y, x)
    result = mstats.siegelslopes(y, x)

    # note both returned values are distinct here
    assert_equal(slope, result.slope)
    assert_equal(intercept, result.intercept)

