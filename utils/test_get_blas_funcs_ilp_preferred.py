
def test_get_blas_funcs_ilp_preferred():
    # "preferred" mean ILP64 if available LP64 otherwise
    gemm = get_blas_funcs('gemm', (np.eye(3),), ilp64="preferred")
    assert gemm.int_dtype == np.int64 if HAS_ILP64 else np.int32
    assert gemm.module_name == 'fblas_64' if HAS_ILP64 else 'fblas'

    # default is "preferred"
    gemm = get_blas_funcs('gemm', (np.eye(3),))
    assert gemm.int_dtype == np.int64 if HAS_ILP64 else np.int32
    assert gemm.module_name == 'fblas_64' if HAS_ILP64 else 'fblas'

