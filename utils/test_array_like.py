
def test_array_like(xp, op):
    x = [[[1.0, 1.0], [1.0, 1.0]],
         [[1.0, 1.0], [1.0, 1.0]],
         [[1.0, 1.0], [1.0, 1.0]]]
    xp_assert_close(op(x, 1.0, 2.0), op(xp.asarray(x), 1.0, 2.0))


def test_array_like(func):
    x = [[[1.0, 1.0], [1.0, 1.0]],
         [[1.0, 1.0], [1.0, 1.0]],
         [[1.0, 1.0], [1.0, 1.0]]]
    xp_assert_close(func(x), func(np.asarray(x)))

