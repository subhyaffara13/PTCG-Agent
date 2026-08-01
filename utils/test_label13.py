
def test_label13(xp):
    for type in types:
        dtype = getattr(xp, type)
        data = xp.asarray([[1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                           [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
                           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                          dtype=dtype)
        out, n = ndimage.label(data)
        expected = [[1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        expected = xp.asarray(expected)
        assert_array_almost_equal(out, expected)
        assert n == 1

