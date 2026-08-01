
def test_get_blas_funcs():
    # check that it returns Fortran code for arrays that are
    # fortran-ordered
    f1, f2, f3 = get_blas_funcs(
        ('axpy', 'axpy', 'axpy'),
        (np.empty((2, 2), dtype=np.complex64, order='F'),
         np.empty((2, 2), dtype=np.complex128, order='C'))
        )

    # get_blas_funcs will choose libraries depending on most generic
    # array
    assert_equal(f1.typecode, 'z')
    assert_equal(f2.typecode, 'z')

    # check defaults.
    f1 = get_blas_funcs('rotg')
    assert_equal(f1.typecode, 'd')

    # check also dtype interface
    f1 = get_blas_funcs('gemm', dtype=np.complex64)
    assert_equal(f1.typecode, 'c')
    f1 = get_blas_funcs('gemm', dtype='F')
    assert_equal(f1.typecode, 'c')

    # extended precision complex
    f1 = get_blas_funcs('gemm', dtype=np.clongdouble)
    assert_equal(f1.typecode, 'z')

    # check safe complex upcasting
    f1 = get_blas_funcs('axpy',
                        (np.empty((2, 2), dtype=np.float64),
                         np.empty((2, 2), dtype=np.complex64))
                        )
    assert_equal(f1.typecode, 'z')

