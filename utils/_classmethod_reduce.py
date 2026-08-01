
def _classmethod_reduce(obj):
    orig_func = obj.__func__
    return type(obj), (orig_func,)

