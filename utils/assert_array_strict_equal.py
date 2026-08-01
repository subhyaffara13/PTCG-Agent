
def assert_array_strict_equal(x, y):
    assert_array_equal(x, y)
    # Check flags, 32 bit arches typically don't provide 16 byte alignment
    if ((x.dtype.alignment <= 8 or
            np.intp().dtype.itemsize != 4) and
            sys.platform != 'win32'):
        assert_(x.flags == y.flags)
    else:
        assert_(x.flags.owndata == y.flags.owndata)
        assert_(x.flags.writeable == y.flags.writeable)
        assert_(x.flags.c_contiguous == y.flags.c_contiguous)
        assert_(x.flags.f_contiguous == y.flags.f_contiguous)
        assert_(x.flags.writebackifcopy == y.flags.writebackifcopy)
    # check endianness
    assert_(x.dtype.isnative == y.dtype.isnative)

