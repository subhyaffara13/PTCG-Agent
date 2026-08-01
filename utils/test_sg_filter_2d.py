
def test_sg_filter_2d(xp):
    x = xp.asarray([[1.0, 2.0, 1.0],
                    [2.0, 4.0, 2.0]])
    expected = xp.asarray([[1.0, 4.0 / 3, 1.0],
                           [2.0, 8.0 / 3, 2.0]])
    y = savgol_filter(x, 3, 1, mode='constant')
    xp_assert_close(y, expected)

    y = savgol_filter(x.T, 3, 1, mode='constant', axis=0)
    xp_assert_close(y, expected.T)

