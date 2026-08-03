import functools

def _tmp_donotuse_dont_inline_everything(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with inline_everything_mode(False):
            fn(*args, **kwargs)
    return wrapper

