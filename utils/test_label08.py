
def test_label08(xp):
    data = xp.asarray([[1, 0, 0, 0, 0, 0],
                       [0, 0, 1, 1, 0, 0],
                       [0, 0, 1, 1, 1, 0],
                       [1, 1, 0, 0, 0, 0],
                       [1, 1, 0, 0, 0, 0],
                       [0, 0, 0, 1, 1, 0]])
    out, n = ndimage.label(data)
    assert_array_almost_equal(out, xp.asarray([[1, 0, 0, 0, 0, 0],
                                               [0, 0, 2, 2, 0, 0],
                                               [0, 0, 2, 2, 2, 0],
                                               [3, 3, 0, 0, 0, 0],
                                               [3, 3, 0, 0, 0, 0],
                                               [0, 0, 0, 4, 4, 0]]))
    assert n == 4

