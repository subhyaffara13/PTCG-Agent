
def skip_if_speedups_missing(func):
    def wrapper(*args, **kwargs):
        if not has_speedups():
            raise unittest.SkipTest("C Extension not available")
        return func(*args, **kwargs)

    return wrapper

