
def test_get_blas_funcs_ilp_false():
    # False is LP64 or fail if not available
    if HAS_LP64_FBLAS:
        gemm = get_blas_funcs('gemm', (np.eye(3),), ilp64=False)
        assert gemm.int_dtype == np.int32
        assert gemm.module_name == 'fblas'
    else:
        with pytest.raises(ValueError):
            get_blas_funcs('gemm', (np.eye(3),), ilp64=False)

