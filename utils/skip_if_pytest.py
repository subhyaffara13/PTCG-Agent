import os

def skip_if_pytest(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if "PYTEST_CURRENT_TEST" in os.environ:
            raise unittest.SkipTest("does not work under pytest")
        return fn(*args, **kwargs)

    return wrapped

