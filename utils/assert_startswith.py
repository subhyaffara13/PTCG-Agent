
def assert_startswith(a, b):
    # produces a better error message than assert_(a.startswith(b))
    assert_equal(a[:len(b)], b)

