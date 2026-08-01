
def initialize_cuda_context_rng():
    global __cuda_ctx_rng_initialized
    if not TEST_CUDA:
        raise AssertionError('CUDA must be available when calling initialize_cuda_context_rng')
    if not __cuda_ctx_rng_initialized:
        # initialize cuda context and rng for memory tests
        for i in range(torch.cuda.device_count()):
            torch.randn(1, device=f"cuda:{i}")
        __cuda_ctx_rng_initialized = True

