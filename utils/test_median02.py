
def test_median02(xp):
    a = xp.asarray([[1, 2, 0, 1],
                    [5, 3, 0, 4],
                    [0, 0, 0, 7],
                    [9, 3, 0, 0]])
    output = ndimage.median(a)
    assert_almost_equal(output, xp.asarray(1.0), check_0d=False)

