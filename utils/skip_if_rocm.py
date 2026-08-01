
def skipIfRocm(func=None, *, msg="test doesn't currently work on the ROCm stack"):
    def dec_fn(fn):
        reason = f"skipIfRocm: {msg}"

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if TEST_WITH_ROCM:
                raise unittest.SkipTest(reason)
            else:
                return fn(*args, **kwargs)
        return wrapper
    if func:
        return dec_fn(func)
    return dec_fn

