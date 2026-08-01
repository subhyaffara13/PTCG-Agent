
def test_boxcox1p_nonfinite():
    # x < -1  =>  y = nan
    x = np.array([-2, -2, -1.5])
    y = boxcox1p(x, [0.5, 2.0, -1.5])
    assert_equal(y, np.array([np.nan, np.nan, np.nan]))

    # x = -1 and lambda <= 0  =>  y = -inf
    x = -1
    y = boxcox1p(x, [-2.5, 0])
    assert_equal(y, np.array([-np.inf, -np.inf]))

