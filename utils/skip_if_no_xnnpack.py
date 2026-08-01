
def skipIfNoXNNPACK(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not torch.backends.xnnpack.enabled:  # type: ignore[attr-defined]
            raise unittest.SkipTest('XNNPACK must be enabled for these tests. Please build with USE_XNNPACK=1.')
        else:
            fn(*args, **kwargs)
    return wrapper

