
def test_boxcox_nonfinite():
    # x < 0  =>  y = nan
    x = np.array([-1, -1, -0.5])
    y = boxcox(x, [0.5, 2.0, -1.5])
    assert_equal(y, np.array([np.nan, np.nan, np.nan]))

    # x = 0 and lambda <= 0  =>  y = -inf
    x = 0
    y = boxcox(x, [-2.5, 0])
    assert_equal(y, np.array([-np.inf, -np.inf]))

