
def skip_if_not_implemented(test_func):
    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        try:
            return test_func(*args, **kwargs)
        except NotImplementedError as e:
            raise unittest.SkipTest(f"Test skipped due to NotImplementedError: {e}")

    return wrapper

