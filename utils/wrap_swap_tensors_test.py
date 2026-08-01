
def wrapSwapTensorsTest(swap=None):
    def dec_fn(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with SwapTensorsGuard(swap):
                fn(*args, **kwargs)
        return wrapper
    return dec_fn

