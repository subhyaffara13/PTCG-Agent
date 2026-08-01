
def test_moment_order_4():
    # gh-13655 reported that if a distribution has a `_stats` method that
    # accepts the `moments` parameter, then if the distribution's `moment`
    # method is called with `order=4`, the faster/more accurate`_stats` gets
    # called, but the results aren't used, and the generic `_munp` method is
    # called to calculate the moment anyway. This tests that the issue has
    # been fixed.
    # stats.skewnorm._stats accepts the `moments` keyword
    stats.skewnorm._stats(a=0, moments='k')  # no failure = has `moments`
    # When `moment` is called, `_stats` is used, so the moment is very accurate
    # (exactly equal to Pearson's kurtosis of the normal distribution, 3)
    assert stats.skewnorm.moment(order=4, a=0) == 3.0
    # At the time of gh-13655, skewnorm._munp() used the generic method
    # to compute its result, which was inefficient and not very accurate.
    # At that time, the following assertion would fail.  skewnorm._munp()
    # has since been made more accurate and efficient, so now this test
    # is expected to pass.
    assert stats.skewnorm._munp(4, 0) == 3.0

