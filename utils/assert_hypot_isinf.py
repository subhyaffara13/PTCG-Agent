
def assert_hypot_isinf(x, y):
    with np.errstate(invalid='ignore'):
        assert_(np.isinf(ncu.hypot(x, y)),
                f"hypot({x}, {y}) is {ncu.hypot(x, y)}, not inf")

