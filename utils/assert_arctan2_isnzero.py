
def assert_arctan2_isnzero(x, y):
    assert_(
        (ncu.arctan2(x, y) == 0 and np.signbit(ncu.arctan2(x, y))),
        f"arctan({x}, {y}) is {ncu.arctan2(x, y)}, not -0",
    )

