
def test_linearoperator_deallocation():
    # Check that the linear operators used by the Arpack wrappers are
    # deallocatable by reference counting -- they are big objects, so
    # Python's cyclic GC may not collect them fast enough before
    # running out of memory if eigs/eigsh are called in a tight loop.

    M_d = np.eye(10)
    M_s = csc_array(M_d)
    M_o = aslinearoperator(M_d)

    with assert_deallocated(lambda: arpack.SpLuInv(M_s)):
        pass
    with assert_deallocated(lambda: arpack.LuInv(M_d)):
        pass
    with assert_deallocated(lambda: arpack.IterInv(M_s)):
        pass
    with assert_deallocated(lambda: arpack.IterOpInv(M_o, None, 0.3)):
        pass
    with assert_deallocated(lambda: arpack.IterOpInv(M_o, M_o, 0.3)):
        pass

