
def test_sum_labels(xp):
    labels = xp.asarray([[1, 2], [2, 4]], dtype=xp.int8)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
        output_sum = ndimage.sum(input, labels=labels, index=xp.asarray([4, 8, 2]))
        output_labels = ndimage.sum_labels(
            input, labels=labels, index=xp.asarray([4, 8, 2]))

        assert xp.all(output_sum == output_labels)
        assert_array_almost_equal(output_labels, xp.asarray([4.0, 0.0, 5.0]))

