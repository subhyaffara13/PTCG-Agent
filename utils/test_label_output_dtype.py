
def test_label_output_dtype(xp):
    data = xp.ones([5])
    for t in types:
        dtype = getattr(xp, t)
        output, n = ndimage.label(data, output=dtype)
        assert_array_almost_equal(output,
                                  xp.ones(output.shape, dtype=output.dtype))
        assert output.dtype == t

