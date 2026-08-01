
def current_blas_handle():
    r"""Return cublasHandle_t pointer to current cuBLAS handle"""
    _lazy_init()
    return torch._C._cuda_getCurrentBlasHandle()

