
def test_gejsv_general(size, dtype, joba, jobu, jobv, jobr, jobp, jobt=0):
    """Test the lapack routine ?gejsv.

    This function tests that a singular value decomposition can be performed
    on the random M-by-N matrix A. The test performs the SVD using ?gejsv
    then performs the following checks:

    * ?gejsv exist successfully (info == 0)
    * The returned singular values are correct
    * `A` can be reconstructed from `u`, `SIGMA`, `v`
    * Ensure that u.T @ u is the identity matrix
    * Ensure that v.T @ v is the identity matrix
    * The reported matrix rank
    * The reported number of singular values
    * If denormalized floats are required

    Notes
    -----
    joba specifies several choices effecting the calculation's accuracy
    Although all arguments are tested, the tests only check that the correct
    solution is returned - NOT that the prescribed actions are performed
    internally.

    jobt is, as of v3.9.0, still experimental and removed to cut down number of
    test cases. However keyword itself is tested externally.
    """
    rng = np.random.RandomState(42)

    # Define some constants for later use:
    m, n = size
    atol = 100 * np.finfo(dtype).eps
    A = generate_random_dtype_array(size, dtype, rng)
    gejsv = get_lapack_funcs('gejsv', dtype=dtype)

    # Set up checks for invalid job? combinations
    # if an invalid combination occurs we set the appropriate
    # exit status.
    lsvec = jobu < 2  # Calculate left singular vectors
    rsvec = jobv < 2  # Calculate right singular vectors
    l2tran = (jobt == 1) and (m == n)
    is_complex = np.iscomplexobj(A)

    invalid_real_jobv = (jobv == 1) and (not lsvec) and (not is_complex)
    invalid_cplx_jobu = (jobu == 2) and not (rsvec and l2tran) and is_complex
    invalid_cplx_jobv = (jobv == 2) and not (lsvec and l2tran) and is_complex

    # Set the exit status to the expected value.
    # Here we only check for invalid combinations, not individual
    # parameters.
    if invalid_cplx_jobu:
        exit_status = -2
    elif invalid_real_jobv or invalid_cplx_jobv:
        exit_status = -3
    else:
        exit_status = 0

    if (jobu > 1) and (jobv == 1):
        assert_raises(Exception, gejsv, A, joba, jobu, jobv, jobr, jobt, jobp)
    else:
        sva, u, v, work, iwork, info = gejsv(A,
                                             joba=joba,
                                             jobu=jobu,
                                             jobv=jobv,
                                             jobr=jobr,
                                             jobt=jobt,
                                             jobp=jobp)

        # Check that ?gejsv exited successfully/as expected
        assert_equal(info, exit_status)

        # If exit_status is non-zero the combination of jobs is invalid.
        # We test this above but no calculations are performed.
        if not exit_status:

            # Check the returned singular values
            sigma = (work[0] / work[1]) * sva[:n]
            assert_allclose(sigma, svd(A, compute_uv=False), atol=atol)

            if jobu == 1:
                # If JOBU = 'F', then u contains the M-by-M matrix of
                # the left singular vectors, including an ONB of the orthogonal
                # complement of the Range(A)
                # However, to recalculate A we are concerned about the
                # first n singular values and so can ignore the latter.
                # TODO: Add a test for ONB?
                u = u[:, :n]

            if lsvec and rsvec:
                assert_allclose(u @ np.diag(sigma) @ v.conj().T, A, atol=atol)
            if lsvec:
                assert_allclose(u.conj().T @ u, np.identity(n), atol=atol)
            if rsvec:
                assert_allclose(v.conj().T @ v, np.identity(n), atol=atol)

            assert_equal(iwork[0], np.linalg.matrix_rank(A))
            assert_equal(iwork[1], np.count_nonzero(sigma))
            # iwork[2] is non-zero if requested accuracy is not warranted for
            # the data. This should never occur for these tests.
            assert_equal(iwork[2], 0)

