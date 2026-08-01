
def check_polyder(p, m, expected, xp):
    dp = _polyder(p, m, xp=xp)
    xp_assert_equal(dp, expected)

