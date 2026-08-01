
def test_uintalignment_and_alignment():
    # alignment code needs to satisfy these requirements:
    #  1. numpy structs match C struct layout
    #  2. ufuncs/casting is safe wrt to aligned access
    #  3. copy code is safe wrt to "uint alidned" access
    #
    # Complex types are the main problem, whose alignment may not be the same
    # as their "uint alignment".
    #
    # This test might only fail on certain platforms, where uint64 alignment is
    # not equal to complex64 alignment. The second 2 tests will only fail
    # for DEBUG=1.

    d1 = np.dtype('u1,c8', align=True)
    d2 = np.dtype('u4,c8', align=True)
    d3 = np.dtype({'names': ['a', 'b'], 'formats': ['u1', d1]}, align=True)

    assert_equal(np.zeros(1, dtype=d1)['f1'].flags['ALIGNED'], True)
    assert_equal(np.zeros(1, dtype=d2)['f1'].flags['ALIGNED'], True)
    assert_equal(np.zeros(1, dtype='u1,c8')['f1'].flags['ALIGNED'], False)

    # check that C struct matches numpy struct size
    s = _multiarray_tests.get_struct_alignments()
    for d, (alignment, size) in zip([d1, d2, d3], s):
        assert_equal(d.alignment, alignment)
        assert_equal(d.itemsize, size)

    # check that ufuncs don't complain in debug mode
    # (this is probably OK if the aligned flag is true above)
    src = np.zeros((2, 2), dtype=d1)['f1']  # 4-byte aligned, often
    np.exp(src)  # assert fails?

    # check that copy code doesn't complain in debug mode
    dst = np.zeros((2, 2), dtype='c8')
    dst[:, 1] = src[:, 1]  # assert in lowlevel_strided_loops fails?

