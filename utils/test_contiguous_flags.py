
def test_contiguous_flags():
    a = np.ones((4, 4, 1))[::2, :, :]
    a = stride_tricks.as_strided(a, strides=a.strides[:2] + (-123,))
    b = np.ones((2, 2, 1, 2, 2)).swapaxes(3, 4)

    def check_contig(a, ccontig, fcontig):
        assert_(a.flags.c_contiguous == ccontig)
        assert_(a.flags.f_contiguous == fcontig)

    # Check if new arrays are correct:
    check_contig(a, False, False)
    check_contig(b, False, False)
    check_contig(np.empty((2, 2, 0, 2, 2)), True, True)
    check_contig(np.array([[[1], [2]]], order='F'), True, True)
    check_contig(np.empty((2, 2)), True, False)
    check_contig(np.empty((2, 2), order='F'), False, True)

    # Check that np.array creates correct contiguous flags:
    check_contig(np.array(a, copy=None), False, False)
    check_contig(np.array(a, copy=None, order='C'), True, False)
    check_contig(np.array(a, ndmin=4, copy=None, order='F'), False, True)

    # Check slicing update of flags and :
    check_contig(a[0], True, True)
    check_contig(a[None, ::4, ..., None], True, True)
    check_contig(b[0, 0, ...], False, True)
    check_contig(b[:, :, 0:0, :, :], True, True)

    # Test ravel and squeeze.
    check_contig(a.ravel(), True, True)
    check_contig(np.ones((1, 3, 1)).squeeze(), True, True)

