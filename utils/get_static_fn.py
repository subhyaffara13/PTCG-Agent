
def get_static_fn(cls, fn):
    return inspect.getattr_static(cls, fn).__func__

