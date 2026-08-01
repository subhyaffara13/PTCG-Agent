
def assert_hypot_isnan(x, y):
    with np.errstate(invalid='ignore'):
        assert_(np.isnan(ncu.hypot(x, y)),
                f"hypot({x}, {y}) is {ncu.hypot(x, y)}, not nan")

