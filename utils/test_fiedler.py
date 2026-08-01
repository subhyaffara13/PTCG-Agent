
def test_fiedler(xp):
    f = fiedler(xp.asarray([]))
    assert xp_size(f) == 0
    assert f.shape == (0, 0)

    f = fiedler(xp.asarray([123.]))
    xp_assert_equal(f, xp.asarray([[0.]]))

    f = fiedler(xp.arange(1, 7))
    des = xp.asarray([[0, 1, 2, 3, 4, 5],
                      [1, 0, 1, 2, 3, 4],
                      [2, 1, 0, 1, 2, 3],
                      [3, 2, 1, 0, 1, 2],
                      [4, 3, 2, 1, 0, 1],
                      [5, 4, 3, 2, 1, 0]])
    xp_assert_equal(f, des)

