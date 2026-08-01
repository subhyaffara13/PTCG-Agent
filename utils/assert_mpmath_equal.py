
def assert_mpmath_equal(*a, **kw):
    d = MpmathData(*a, **kw)
    d.check()

