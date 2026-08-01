
def test_iter_allocate_output_types_byte_order():
    # Verify the rules for byte order changes

    # When there's just one input, the output type exactly matches
    a = array([3], dtype='u4')
    a = a.view(a.dtype.newbyteorder())
    i = nditer([a, None], [],
                    [['readonly'], ['writeonly', 'allocate']])
    assert_equal(i.dtypes[0], i.dtypes[1])
    # With two or more inputs, the output type is in native byte order
    i = nditer([a, a, None], [],
                    [['readonly'], ['readonly'], ['writeonly', 'allocate']])
    assert_(i.dtypes[0] != i.dtypes[2])
    assert_equal(i.dtypes[0].newbyteorder('='), i.dtypes[2])

