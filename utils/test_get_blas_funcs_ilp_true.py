
def test_get_blas_funcs_ilp_true():
    # True is ILP64 or fail if not available
    if HAS_ILP64:
        gemm = get_blas_funcs('gemm', (np.eye(3),), ilp64=True)
        assert gemm.int_dtype == np.int64
        assert gemm.module_name == 'fblas_64'
    else:
        with pytest.raises(RuntimeError):
            get_blas_funcs('gemm', (np.eye(3),), ilp64=True)

