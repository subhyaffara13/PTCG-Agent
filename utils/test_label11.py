
def test_label11(xp):
    for type in types:
        dtype = getattr(xp, type)
        data = xp.asarray([[1, 0, 0, 0, 0, 0],
                           [0, 0, 1, 1, 0, 0],
                           [0, 0, 1, 1, 1, 0],
                           [1, 1, 0, 0, 0, 0],
                           [1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 1, 1, 0]], dtype=dtype)
        out, n = ndimage.label(data)
        expected = [[1, 0, 0, 0, 0, 0],
                    [0, 0, 2, 2, 0, 0],
                    [0, 0, 2, 2, 2, 0],
                    [3, 3, 0, 0, 0, 0],
                    [3, 3, 0, 0, 0, 0],
                    [0, 0, 0, 4, 4, 0]]
        expected = xp.asarray(expected)
        assert_array_almost_equal(out, expected)
        assert n == 4

