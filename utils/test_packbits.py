
def test_packbits():
    # Copied from the docstring.
    a = [[[1, 0, 1], [0, 1, 0]],
         [[1, 1, 0], [0, 0, 1]]]
    for dt in '?bBhHiIlLqQ':
        arr = np.array(a, dtype=dt)
        b = np.packbits(arr, axis=-1)
        assert_equal(b.dtype, np.uint8)
        assert_array_equal(b, np.array([[[160], [64]], [[192], [32]]]))

    assert_raises(TypeError, np.packbits, np.array(a, dtype=float))

