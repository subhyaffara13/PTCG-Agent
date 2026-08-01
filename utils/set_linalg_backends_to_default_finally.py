
def setLinalgBackendsToDefaultFinally(fn):
    @wraps(fn)
    def _fn(*args, **kwargs):
        _preferred_backend = torch.backends.cuda.preferred_linalg_library()
        try:
            fn(*args, **kwargs)
        finally:
            torch.backends.cuda.preferred_linalg_library(_preferred_backend)
    return _fn

