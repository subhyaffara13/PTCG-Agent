
def test_blas64_geqrf_lwork_smoketest():
    # Smoke test LAPACK geqrf lwork call with 64-bit integers
    dtype = np.float64
    lapack_routine = np.linalg.lapack_lite.dgeqrf

    m = 2**32 + 1
    n = 2**32 + 1
    lda = m

    # Dummy arrays, not referenced by the lapack routine, so don't
    # need to be of the right size
    a = np.zeros([1, 1], dtype=dtype)
    work = np.zeros([1], dtype=dtype)
    tau = np.zeros([1], dtype=dtype)

    # Size query
    results = lapack_routine(m, n, a, lda, tau, work, -1, 0)
    assert_equal(results['info'], 0)
    assert_equal(results['m'], m)
    assert_equal(results['n'], m)

    # Should result to an integer of a reasonable size
    lwork = int(work.item())
    assert_(2**32 < lwork < 2**42)

