
def setBlasBackendsToDefaultFinally(fn):
    @wraps(fn)
    def _fn(*args, **kwargs):
        _preferred_backend = torch.backends.cuda.preferred_blas_library()
        try:
            fn(*args, **kwargs)
        finally:
            torch.backends.cuda.preferred_blas_library(_preferred_backend)
    return _fn

