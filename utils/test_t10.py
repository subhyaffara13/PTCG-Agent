
def test_T10():
    # No longer raises PoleError, but should return euler-mascheroni constant
    assert limit(zeta(x) - 1/(x - 1), x, 1) == integrate(-1/x + 1/floor(x), (x, 1, oo))

