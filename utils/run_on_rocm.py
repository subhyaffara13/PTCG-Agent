
def runOnRocm(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if TEST_WITH_ROCM:
            fn(*args, **kwargs)
        else:
            raise unittest.SkipTest("test currently only works on the ROCm stack")
    return wrapper

