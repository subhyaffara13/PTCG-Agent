
def test_mean04(xp):
    labels = xp.asarray([[1, 2], [2, 4]], dtype=xp.int8)
    with np.errstate(all='ignore'):
        for type in types:
            dtype = getattr(xp, type)
            input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
            output = ndimage.mean(input, labels=labels,
                                  index=xp.asarray([4, 8, 2]))
            # XXX: output[[0, 2]] does not work in array-api-strict; annoying
            # assert_array_almost_equal(output[[0, 2]], xp.asarray([4.0, 2.5]))
            assert output[0] == 4.0
            assert output[2] == 2.5
            assert xp.isnan(output[1])

