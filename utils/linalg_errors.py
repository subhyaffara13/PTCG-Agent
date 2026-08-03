import functools

def linalg_errors(func):
    @functools.wraps(func)
    def wrapped(*args, **kwds):
        try:
            return func(*args, **kwds)
        except torch._C._LinAlgError as e:
            raise LinAlgError(*e.args)  # noqa: B904

    return wrapped

