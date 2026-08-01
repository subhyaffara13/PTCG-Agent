
def skipIfCrossRef(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if TEST_WITH_CROSSREF:
            raise unittest.SkipTest("test doesn't currently with crossref")
        else:
            fn(*args, **kwargs)
    return wrapper

