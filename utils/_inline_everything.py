
def _inline_everything(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with inline_everything_mode(True):
            fn(*args, **kwargs)
    return wrapper

