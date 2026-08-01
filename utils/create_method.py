
def create_method(fn, name=None):
    name = name or fn.__name__

    def f(*args, **kwargs):
        return fn(*args, **kwargs)

    f.__name__ = name
    f.__qualname__ = f"ndarray.{name}"
    return f

