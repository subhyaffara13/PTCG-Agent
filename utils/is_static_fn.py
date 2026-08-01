
def is_static_fn(cls, fn) -> bool:
    return isinstance(inspect.getattr_static(cls, fn, default=None), staticmethod)

