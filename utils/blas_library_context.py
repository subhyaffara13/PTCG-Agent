
def blas_library_context(backend):
    prev_backend = torch.backends.cuda.preferred_blas_library()
    torch.backends.cuda.preferred_blas_library(backend)
    try:
        yield
    finally:
        torch.backends.cuda.preferred_blas_library(prev_backend)

