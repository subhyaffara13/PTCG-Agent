
def _call_method(method, rref, *args, **kwargs):
    return method(rref.local_value(), *args, **kwargs)


def _call_method(method, obj_rref, *args, **kwargs):
    return method(obj_rref.local_value(), *args, **kwargs)


def _call_method(method, rref, *args, **kwargs):
    r"""
    a helper function to call a method on the given RRef
    """
    return method(rref.local_value(), *args, **kwargs)

