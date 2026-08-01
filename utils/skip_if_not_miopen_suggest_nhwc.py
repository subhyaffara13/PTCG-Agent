
def skipIfNotMiopenSuggestNHWC(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not TEST_WITH_MIOPEN_SUGGEST_NHWC:
            raise unittest.SkipTest("test doesn't currently work without MIOpen NHWC activation")
        else:
            fn(*args, **kwargs)
    return wrapper

