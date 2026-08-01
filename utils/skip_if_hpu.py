
def skipIfHpu(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if TEST_HPU:
            raise unittest.SkipTest("test doesn't currently work with HPU")
        else:
            fn(*args, **kwargs)
    return wrapper

