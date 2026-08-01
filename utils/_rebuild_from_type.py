
def _rebuild_from_type(func, type, args, dict):
    if type is Tensor:
        return func(*args)

    ret = func(*args).as_subclass(type)
    ret.__dict__ = dict
    return ret

