
def test_reentering():
    # Just some linear operator that calls eigs recursively
    def A_matvec(x):
        x = diags_array([1.0, -2.0, 1.0], offsets=[-1, 0, 1], shape=(50, 50))
        w, v = eigs(x, k=1)
        return v.real / w[0].real
    A = LinearOperator(matvec=A_matvec, dtype=float, shape=(50, 50))

    # ================= Old Fortran tests ==================
    # The Fortran code is not reentrant, so this fails (gracefully, not crashing)
    # assert_raises(RuntimeError, eigs, A, k=1)
    # assert_raises(RuntimeError, eigsh, A, k=1)
    #
    # These should not crash upon reentrance
    eigs(A, k=1)
    eigsh(A, k=1)

