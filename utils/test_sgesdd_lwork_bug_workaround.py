
def test_sgesdd_lwork_bug_workaround():
    # Test that SGESDD lwork is sufficiently large for LAPACK.
    #
    # This checks that _compute_lwork() correctly works around a bug in
    # LAPACK versions older than 3.10.1.

    sgesdd_lwork = get_lapack_funcs('gesdd_lwork', dtype=np.float32,
                                    ilp64='preferred')
    n = 9537
    lwork = _compute_lwork(sgesdd_lwork, n, n,
                           compute_uv=True, full_matrices=True)
    # If we called the Fortran function SGESDD directly with IWORK=-1, the
    # LAPACK bug would result in lwork being 272929856, which was too small.
    # (The result was returned in a single precision float, which does not
    # have sufficient precision to represent the exact integer value that it
    # computed internally.)  The work-around implemented in _compute_lwork()
    # will convert that to 272929888.  If we are using LAPACK 3.10.1 or later
    # (such as in OpenBLAS 0.3.21 or later), the work-around will return
    # 272929920, because it does not know which version of LAPACK is being
    # used, so it always applies the correction to whatever it is given.  We
    # will accept either 272929888 or 272929920.
    # Note that the acceptable values are a LAPACK implementation detail.
    # If a future version of LAPACK changes how SGESDD works, and therefore
    # changes the required LWORK size, the acceptable values might have to
    # be updated.
    assert lwork == 272929888 or lwork == 272929920

