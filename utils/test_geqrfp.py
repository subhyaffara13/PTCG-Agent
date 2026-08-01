
def test_geqrfp(dtype, matrix_size):
    # Tests for all dytpes, tall, wide, and square matrices.
    # Using the routine with random matrix A, Q and R are obtained and then
    # tested such that R is upper triangular and non-negative on the diagonal,
    # and Q is an orthogonal matrix. Verifies that A=Q@R. It also
    # tests against a matrix that for which the  linalg.qr method returns
    # negative diagonals, and for error messaging.

    # set test tolerance appropriate for dtype
    rng = np.random.RandomState(42)
    rtol = 250*np.finfo(dtype).eps
    atol = 100*np.finfo(dtype).eps
    # get appropriate ?geqrfp for dtype
    geqrfp = get_lapack_funcs(('geqrfp'), dtype=dtype)
    gqr = get_lapack_funcs(("orgqr"), dtype=dtype)

    m, n = matrix_size

    # create random matrix of dimensions m x n
    A = generate_random_dtype_array((m, n), dtype=dtype, rng=rng)
    # create qr matrix using geqrfp
    qr_A, tau, info = geqrfp(A)

    # obtain r from the upper triangular area
    r = np.triu(qr_A)

    # obtain q from the orgqr lapack routine
    # based on linalg.qr's extraction strategy of q with orgqr

    if m > n:
        # this adds an extra column to the end of qr_A
        # let qqr be an empty m x m matrix
        qqr = np.zeros((m, m), dtype=dtype)
        # set first n columns of qqr to qr_A
        qqr[:, :n] = qr_A
        # determine q from this qqr
        # note that m is a sufficient for lwork based on LAPACK documentation
        q = gqr(qqr, tau=tau, lwork=m)[0]
    else:
        q = gqr(qr_A[:, :m], tau=tau, lwork=m)[0]

    # test that q and r still make A
    assert_allclose(q@r, A, rtol=rtol)
    # ensure that q is orthogonal (that q @ transposed q is the identity)
    assert_allclose(np.eye(q.shape[0]), q@(q.conj().T), rtol=rtol,
                    atol=atol)
    # ensure r is upper tri by comparing original r to r as upper triangular
    assert_allclose(r, np.triu(r), rtol=rtol)
    # make sure diagonals of r are positive for this random solution
    assert_(np.all(np.diag(r) > np.zeros(len(np.diag(r)))))
    # ensure that info is zero for this success
    assert_(info == 0)

    # test that this routine gives r diagonals that are positive for a
    # matrix that returns negatives in the diagonal with scipy.linalg.rq
    A_negative = generate_random_dtype_array((n, m), dtype=dtype, rng=rng) * -1
    r_rq_neg, q_rq_neg = qr(A_negative)
    rq_A_neg, tau_neg, info_neg = geqrfp(A_negative)
    # assert that any of the entries on the diagonal from linalg.qr
    #   are negative and that all of geqrfp are positive.
    assert_(np.any(np.diag(r_rq_neg) < 0) and
            np.all(np.diag(r) > 0))

