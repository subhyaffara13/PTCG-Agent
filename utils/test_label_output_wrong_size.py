
def test_label_output_wrong_size(xp):
    data = xp.ones([5])
    for t in types:
        dtype = getattr(xp, t)
        output = xp.zeros([10], dtype=dtype)
        assert_raises(ValueError, ndimage.label, data, output=output)

