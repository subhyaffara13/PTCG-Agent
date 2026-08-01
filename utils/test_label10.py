
def test_label10(xp):
    data = xp.asarray([[0, 0, 0, 0, 0, 0],
                       [0, 1, 1, 0, 1, 0],
                       [0, 1, 1, 1, 1, 0],
                       [0, 0, 0, 0, 0, 0]])
    struct = ndimage.generate_binary_structure(2, 2)
    struct = xp.asarray(struct)
    out, n = ndimage.label(data, struct)
    assert_array_almost_equal(out, xp.asarray([[0, 0, 0, 0, 0, 0],
                                               [0, 1, 1, 0, 1, 0],
                                               [0, 1, 1, 1, 1, 0],
                                               [0, 0, 0, 0, 0, 0]]))
    assert n == 1

