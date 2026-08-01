
def _jit_unwrap_structured(obj):
    if hasattr(obj, "_jit_unwrap"):
        return obj._jit_unwrap()
    return obj

