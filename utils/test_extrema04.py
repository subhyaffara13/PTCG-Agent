
def test_extrema04(xp):
    labels = xp.asarray([1, 2, 0, 4])
    for type in types:
        if is_torch(xp) and type in ("uint16", "uint32", "uint64"):
             pytest.xfail("https://github.com/pytorch/pytorch/issues/58734")

        dtype = getattr(xp, type)
        input = xp.asarray([[5, 4, 2, 5],
                            [3, 7, 8, 2],
                            [1, 5, 1, 1]], dtype=dtype)
        output1 = ndimage.extrema(input, labels, xp.asarray([1, 2]))
        output2 = ndimage.minimum(input, labels, xp.asarray([1, 2]))
        output3 = ndimage.maximum(input, labels, xp.asarray([1, 2]))
        output4 = ndimage.minimum_position(input, labels,
                                           xp.asarray([1, 2]))
        output5 = ndimage.maximum_position(input, labels,
                                           xp.asarray([1, 2]))
        assert_array_almost_equal(output1[0], output2)
        assert_array_almost_equal(output1[1], output3)
        assert output1[2] == output4
        assert output1[3] == output5

