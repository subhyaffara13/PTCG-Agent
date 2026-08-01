
def skipIfNoSciPy(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not TEST_SCIPY:
            raise unittest.SkipTest("test require SciPy, but SciPy not found")
        else:
            fn(*args, **kwargs)
    return wrapper

