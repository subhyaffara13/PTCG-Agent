
def xfailIfSM89PreCUDA13(func):
    """xfail on SM89 only for CUDA < 13. On CUDA 13+, test should pass on all architectures."""
    if IS_SM89 and _get_torch_cuda_version() < (13, 0):
        return unittest.expectedFailure(func)
    return func

