
def test_extrema03(xp):
    labels = xp.asarray([[1, 2], [2, 3]])
    for type in types:
        if is_torch(xp) and type in ("uint16", "uint32", "uint64"):
             pytest.xfail("https://github.com/pytorch/pytorch/issues/58734")

        dtype = getattr(xp, type)
        input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
        output1 = ndimage.extrema(input,
                                  labels=labels,
                                  index=xp.asarray([2, 3, 8]))
        output2 = ndimage.minimum(input,
                                  labels=labels,
                                  index=xp.asarray([2, 3, 8]))
        output3 = ndimage.maximum(input, labels=labels,
                                  index=xp.asarray([2, 3, 8]))
        output4 = ndimage.minimum_position(input,
                                           labels=labels,
                                           index=xp.asarray([2, 3, 8]))
        output5 = ndimage.maximum_position(input,
                                           labels=labels,
                                           index=xp.asarray([2, 3, 8]))
        assert_array_almost_equal(output1[0], output2)
        assert_array_almost_equal(output1[1], output3)
        assert output1[2] == output4
        assert output1[3] == output5

