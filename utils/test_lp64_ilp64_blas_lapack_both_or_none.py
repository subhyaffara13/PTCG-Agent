
def test_lp64_ilp64_blas_lapack_both_or_none():
    from scipy.linalg.blas import HAS_ILP64 as blas_has_ilp64
    from scipy.linalg.lapack import HAS_ILP64 as lapack_has_ilp64
    assert blas_has_ilp64 == lapack_has_ilp64

    from scipy.linalg.blas import HAS_LP64 as blas_has_lp64
    from scipy.linalg.lapack import HAS_LP64 as lapack_has_lp64
    assert blas_has_lp64 == lapack_has_lp64

