
def test_dnrm2_neg_incx():
    # check that dnrm2(..., incx < 0) raises
    # XXX: remove the test after the lowest supported BLAS implements
    # negative incx (new in LAPACK 3.10)
    x = np.repeat(10, 9)
    incx = -1
    dnrm2 = scipy.linalg.blas.get_blas_funcs('nrm2', (x,), ilp64='preferred')
    with assert_raises(FBLAS_ERROR):
        dnrm2(x, 5, 3, incx)

