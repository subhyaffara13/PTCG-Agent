
def test_label_output_typed(xp):
    data = xp.ones([5])
    for t in types:
        dtype = getattr(xp, t)
        output = xp.zeros([5], dtype=dtype)
        n = ndimage.label(data, output=output)
        assert_array_almost_equal(output,
                                  xp.ones(output.shape, dtype=output.dtype))
        assert n == 1

