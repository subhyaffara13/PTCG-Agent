
def assert_arctan2_isninf(x, y):
    assert_(
        (np.isinf(ncu.arctan2(x, y)) and ncu.arctan2(x, y) < 0),
        f"arctan({x}, {y}) is {ncu.arctan2(x, y)}, not -inf",
    )

