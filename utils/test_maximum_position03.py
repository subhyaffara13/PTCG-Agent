
def test_maximum_position03(xp):
    input = np.asarray([[5, 4, 2, 5],
                        [3, 7, 8, 2],
                        [1, 5, 1, 1]], dtype=bool)
    input = xp.asarray(input)
    output = ndimage.maximum_position(input)
    assert output == (0, 0)

