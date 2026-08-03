import functools

def _disable_prexisiting_fake_mode(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with unset_fake_temporarily():
            return fn(*args, **kwargs)

    return wrapper

