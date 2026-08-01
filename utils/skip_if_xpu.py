
def skipIfXpu(func=None, *, msg="test doesn't currently work on the XPU stack"):
    def dec_fn(fn):
        reason = f"skipIfXpu: {msg}"

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if TEST_XPU:
                raise unittest.SkipTest(reason)
            else:
                return fn(*args, **kwargs)
        return wrapper
    if func:
        return dec_fn(func)
    return dec_fn

