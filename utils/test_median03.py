
def test_median03(xp):
    a = xp.asarray([[1, 2, 0, 1],
                    [5, 3, 0, 4],
                    [0, 0, 0, 7],
                    [9, 3, 0, 0]])
    labels = xp.asarray([[1, 1, 0, 2],
                         [1, 1, 0, 2],
                         [0, 0, 0, 2],
                         [3, 3, 0, 0]])
    output = ndimage.median(a, labels=labels)
    assert_almost_equal(output, xp.asarray(3.0), check_0d=False)

