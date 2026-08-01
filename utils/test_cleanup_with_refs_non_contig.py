
def test_cleanup_with_refs_non_contig():
    # Regression test, leaked the dtype (but also good for rest)
    dtype = np.dtype("O,i")
    obj = object()
    expected_ref_dtype = sys.getrefcount(dtype)
    expected_ref_obj = sys.getrefcount(obj)
    proto = np.full((3, 4, 5, 6, 7), np.array((obj, 2), dtype=dtype))
    # Give array a non-trivial order to exercise more cleanup paths.
    arr = proto.transpose((2, 0, 3, 1, 4)).copy("K")
    del proto, arr

    actual_ref_dtype = sys.getrefcount(dtype)
    actual_ref_obj = sys.getrefcount(obj)
    assert actual_ref_dtype == expected_ref_dtype
    assert actual_ref_obj == actual_ref_dtype

