
def skipIfNoXPU(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not TEST_XPU:
            raise unittest.SkipTest("test required PyTorched compiled with XPU")
        else:
            fn(*args, **kwargs)
    return wrapper

