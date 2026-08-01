
def test_minimum_position04(xp):
    input = np.asarray([[5, 4, 2, 5],
                        [3, 7, 1, 2],
                        [1, 5, 1, 1]], dtype=bool)
    input = xp.asarray(input)
    output = ndimage.minimum_position(input)
    assert output == (0, 0)

