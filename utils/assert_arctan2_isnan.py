
def assert_arctan2_isnan(x, y):
    assert_(
        np.isnan(ncu.arctan2(x, y)),
        f"arctan({x}, {y}) is {ncu.arctan2(x, y)}, not nan",
    )

