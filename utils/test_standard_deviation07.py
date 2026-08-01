
def test_standard_deviation07(xp):
    labels = xp.asarray([1])
    with np.errstate(all='ignore'):
        for type in types:
            if is_torch(xp) and type == 'uint8':
                pytest.xfail("value cannot be converted to type uint8 "
                             "without overflow")
            dtype = getattr(xp, type)
            input = xp.asarray([-0.00619519], dtype=dtype)
            output = ndimage.standard_deviation(input, labels, xp.asarray([1]))
            assert_array_almost_equal(output, xp.asarray([0]))

