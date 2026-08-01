
def test_b_orthonormalize(n, m, Vdtype, Bdtype, BVdtype):
    """Test B-orthonormalization by Cholesky with callable 'B'.
    The function '_b_orthonormalize' is key in LOBPCG but may
    lead to numerical instabilities. The input vectors are often
    badly scaled, so the function needs scale-invariant Cholesky;
    see https://netlib.org/lapack/lawnspdf/lawn14.pdf.
    """
    rnd = np.random.RandomState(0)
    X = rnd.standard_normal((n, m)).astype(Vdtype)
    Xcopy = np.copy(X)
    vals = np.arange(1, n+1, dtype=float)
    B = dia_array(([vals], [0]), shape=(n, n)).astype(Bdtype)
    BX = B @ X
    BX = BX.astype(BVdtype)
    is_all_complex = (np.issubdtype(Vdtype, np.complexfloating) and
                     np.issubdtype(BVdtype, np.complexfloating))
    is_all_notcomplex = (not np.issubdtype(Vdtype, np.complexfloating) and
                        not np.issubdtype(Bdtype, np.complexfloating) and
                        not np.issubdtype(BVdtype, np.complexfloating))

    # All complex or all not complex can calculate in-place
    check_inplace = is_all_complex or is_all_notcomplex
    # np.longdouble tol cannot be achieved on most systems
    atol = m * n * max(np.finfo(Vdtype).eps,
                       np.finfo(BVdtype).eps,
                       np.finfo(np.float64).eps)

    Xo, BXo, _ = _b_orthonormalize(lambda v: B @ v, X, BX)
    if check_inplace:
        # Check in-place
        assert_equal(X, Xo)
        assert_equal(id(X), id(Xo))
        assert_equal(BX, BXo)
        assert_equal(id(BX), id(BXo))
    # Check BXo
    assert_allclose(B @ Xo, BXo, atol=atol, rtol=atol)
    # Check B-orthonormality
    assert_allclose(Xo.T.conj() @ B @ Xo, np.identity(m),
                    atol=atol, rtol=atol)
    # Repeat without BX in outputs
    X = np.copy(Xcopy)
    Xo1, BXo1, _ = _b_orthonormalize(lambda v: B @ v, X)
    assert_allclose(Xo, Xo1, atol=atol, rtol=atol)
    assert_allclose(BXo, BXo1, atol=atol, rtol=atol)
    if check_inplace:
        # Check in-place.
        assert_equal(X, Xo1)
        assert_equal(id(X), id(Xo1))
    # Check BXo1
    assert_allclose(B @ Xo1, BXo1, atol=atol, rtol=atol)

    # Introduce column-scaling in X
    scaling = 1.0 / np.geomspace(10, 1e10, num=m)
    X = Xcopy * scaling
    X = X.astype(Vdtype)
    BX = B @ X
    BX = BX.astype(BVdtype)
    # Check scaling-invariance of Cholesky-based orthonormalization
    # XXX: internally, _b_orthonormalize tries to invert an ill-conditioned matrix
    Xo1, BXo1, _ = _b_orthonormalize(lambda v: B @ v, X, BX)
    # The output should be the same, up the signs of the columns
    Xo1 =  sign_align(Xo1, Xo)
    assert_allclose(Xo, Xo1, atol=atol, rtol=atol)
    BXo1 =  sign_align(BXo1, BXo)
    assert_allclose(BXo, BXo1, atol=atol, rtol=atol)

