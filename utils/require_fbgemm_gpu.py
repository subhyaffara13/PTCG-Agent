
def require_fbgemm_gpu(test_case):
    """
    Decorator for fbgemm_gpu dependency
    """
    return unittest.skipUnless(is_fbgemm_gpu_available(), "test requires fbgemm-gpu")(test_case)

