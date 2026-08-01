
def skipIfWindows(func=None, *, msg="test doesn't currently work on the Windows stack"):
    def dec_fn(fn):
        reason = f"skipIfWindows: {msg}"

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if IS_WINDOWS:  # noqa: F821
                raise unittest.SkipTest(reason)
            else:
                return fn(*args, **kwargs)
        return wrapper
    if func:
        return dec_fn(func)
    return dec_fn

